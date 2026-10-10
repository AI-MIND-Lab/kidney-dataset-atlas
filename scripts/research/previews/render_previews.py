#!/usr/bin/env python
"""render_previews.py: draw the 17 kidney CT preview figures (KiTS23, RMaC, TCGA-KIRC).

What it does
    Draws each preview from its CT volume(s) and mask. A KiTS23 or TCGA-KIRC figure
    has four panels: the axial slice where the centred label (tumour, or cyst for
    *_cyst files) is largest, a zoom on the labelled structures (25-voxel margin), and
    coronal and sagittal cuts through the label's centre at true physical
    proportions. An RMaC figure shows the exam's phases registered to the
    non-contrast grid, all at the tumour's largest slice and the same zoom (40-voxel
    margin). Window level 50 / width 500 HU (-200 to 300 HU); radiological
    orientation (patient left on the viewer's right, anterior and superior at the
    top); nearest-neighbour display; outlines kidney green (lime), tumour red, cyst
    yellow, drawn with matplotlib's contour at 0.5. Default --scale 2 gives 2x the
    original pixel size (220 DPI); --scale 1 gives the original 110-DPI figures.
    Output is deterministic: the same inputs give byte-identical PNG files.

Datasets and files it reads (only these; it holds no data, downloads nothing and
writes only into --out-dir)
    KiTS23  --kits23-dir      images/<case>.nii.gz and segmentations/<case>.nii.gz from
                              the KiTS23 release (labels 1 kidney, 2 tumour, 3 cyst),
                              reoriented to LPS on load.
    RMaC    --rmac-dir        volumes/<exam>/{noncon,arterial,portven,delay}.nii.gz and
                              masks/<exam>/mask_RMaC.nii.gz: the phases and tumour mask
                              of the exam's UCSF RMaC HDF5 file, converted to LPS NIfTI
                              by renal-clip-rmac's scripts/process_datasets.py.
    TCGA    --tcga-ct-dir     <patient>/<series UID>_b<block>.nii.gz: TCGA-KIRC CT
                              series converted from TCIA DICOM to LPS NIfTI by the same
                              script.
            --tcga-bamf-dir   <patient>/<series UID>_b<block>_BAMF.nii.gz: the BAMF
                              (TCIA) mask on that volume's grid.
            --tcga-rccaid-dir <patient>/<series UID>_b<block>_RCC-AID.nii.gz: the
                              RCC-AID mask on that volume's grid.
    In renal-clip-rmac these are data/kits23/hf, data/processed/rmac,
    data/processed/tcga/volumes, and data/processed/tcga/masks for both mask folders.

How to run (one dataset at a time, or --dataset all with every folder)
    python render_previews.py --dataset kits23 --kits23-dir KITS --out-dir OUT
    python render_previews.py --dataset rmac --rmac-dir RMAC --out-dir OUT
    python render_previews.py --dataset tcga --tcga-ct-dir CT --tcga-bamf-dir BAMF \\
        --tcga-rccaid-dir RCCAID --out-dir OUT
    Add --scale 1 for the original size, and --compare-to DIR to check each output
    pixel by pixel against an existing figure set with the same layout (exit status 1
    if any differ or are missing). Figures go to OUT/{kits23,rmac,tcga}/<name>.png.

Requirements: requirements.txt next to this file (Python 3.11.13).
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # write nothing outside --out-dir, not even __pycache__

import argparse  # noqa: E402
import os  # noqa: E402
import tempfile  # noqa: E402
from pathlib import Path  # noqa: E402
from typing import NamedTuple  # noqa: E402

import numpy as np  # noqa: E402
import SimpleITK as sitk  # noqa: E402

BASE_DPI = 110  # the original figures; --scale multiplies it
LO, HI = -200, 300  # level 50 HU, width 500 HU
LABELS = {1: ("kidney", "lime"), 2: ("tumour", "red"), 3: ("cyst", "yellow")}
FOCUS = {"tumour": 2, "cyst": 3}


# --- per-case choices --------------------------------------------------------------------

# KiTS23: (case, centred label). All were drawn with the "| centred on the ..." title.
KITS23 = [
    ("case_00062", "tumour"),
    ("case_00236", "tumour"),
    ("case_00242", "tumour"),
    ("case_00242", "cyst"),
    ("case_00203", "cyst"),
    ("case_00433", "cyst"),
]

# RMaC: exam -> phases registered to the non-contrast grid (registration code 2), in
# display order. The mask is the exam's tumour mask, drawn on the non-contrast grid.
RMAC = {
    "3LYUFVSwiY": ("non-contrast", "arterial", "delayed"),
    "YoPBh7znuG": ("non-contrast", "venous", "delayed"),
    "Mnx1XxZZPN": ("non-contrast", "arterial", "venous", "delayed"),
    "WC3J7Q0yat": ("non-contrast", "arterial", "venous", "delayed"),
}
RMAC_FILE = {
    "non-contrast": "noncon",
    "arterial": "arterial",
    "venous": "portven",
    "delayed": "delay",
}


class TcgaCase(NamedTuple):
    patient: str
    focus: str  # centred label
    series: str  # volume file stem: <series UID>_b<block>
    mask: str  # "BAMF" or "RCC-AID"
    phase: str  # phase shown in the title
    phase_source: str  # who assigned the phase, shown in the title
    manufacturer: str  # scanner manufacturer, shown in the title
    centred_title: bool  # title ends "| centred on the ..." (False: earlier figure version)


# fmt: off
TCGA = [
    TcgaCase("TCGA-BP-5200", "tumour", "1.3.6.1.4.1.14519.5.2.1.9203.4004.116147284150732988858354426071_b1", "BAMF", "venous", "reader", "GE MEDICAL SYSTEMS", False),
    TcgaCase("TCGA-CJ-6033", "tumour", "1.3.6.1.4.1.14519.5.2.1.1706.4004.113074681029142829326799418306_b0", "BAMF", "arterial", "reader", "GE MEDICAL SYSTEMS", False),
    TcgaCase("TCGA-CJ-4918", "cyst", "1.3.6.1.4.1.14519.5.2.1.1706.4004.252007142387318994840525680708_b0", "BAMF", "arterial", "reader", "GE MEDICAL SYSTEMS", True),
    TcgaCase("TCGA-CJ-5677", "cyst", "1.3.6.1.4.1.14519.5.2.1.1706.4004.252183588906413398306019537863_b0", "BAMF", "arterial", "reader", "GE MEDICAL SYSTEMS", True),
    TcgaCase("TCGA-CZ-5984", "tumour", "1.3.6.1.4.1.14519.5.2.1.3671.4004.442517135658683516013972318650_b0", "RCC-AID", "delayed", "reader", "SIEMENS", False),
    TcgaCase("TCGA-DV-5574", "tumour", "1.3.6.1.4.1.14519.5.2.1.1357.4004.370863745597472639438901714146_b0", "RCC-AID", "arterial", "reader", "Philips", False),
    TcgaCase("TCGA-B8-5158", "cyst", "1.3.6.1.4.1.14519.5.2.1.8421.4004.135865630411581743002213655570_b0", "RCC-AID", "delayed", "reader", "SIEMENS", True),
]
# fmt: on


# --- drawing -------------------------------------------------------------------------------

plt = None  # matplotlib.pyplot, imported by setup_matplotlib() once --out-dir is known


def setup_matplotlib(config_dir: str) -> None:
    """Import matplotlib with its config and font cache in `config_dir`, at default settings."""
    global plt
    os.environ["MPLCONFIGDIR"] = config_dir  # no font cache written outside --out-dir
    import matplotlib

    matplotlib.rcdefaults()  # ignore any matplotlibrc on the machine
    matplotlib.use("Agg")
    import matplotlib.pyplot

    plt = matplotlib.pyplot


def load(path: Path, lps: bool = False) -> tuple[np.ndarray, tuple[float, float, float]]:
    image = sitk.ReadImage(str(path))
    if lps:  # KiTS23 files are not in LPS
        image = sitk.DICOMOrient(image, "LPS")
    return sitk.GetArrayFromImage(image), image.GetSpacing()  # (z, y, x); (x, y, z)


def focus(mask: np.ndarray, label: int) -> tuple[int, int, int]:
    """Slice with the largest area of `label`, and the label's median centre (z, y, x)."""
    target = mask == label if (mask == label).any() else mask > 0
    z = int(np.argmax(target.sum(axis=(1, 2))))
    _, yy, xx = np.nonzero(target)
    return z, int(np.median(yy)), int(np.median(xx))


def zoom_box(msk2d: np.ndarray, margin: int) -> tuple[slice, slice]:
    ys, xs = np.nonzero(msk2d > 0)
    if ys.size == 0:
        return slice(None), slice(None)
    return (
        slice(max(ys.min() - margin, 0), ys.max() + margin),
        slice(max(xs.min() - margin, 0), xs.max() + margin),
    )


def show(ax, img, msk, aspect=1.0, title="") -> None:  # type: ignore[no-untyped-def]
    ax.imshow(img, cmap="gray", vmin=LO, vmax=HI, aspect=aspect, interpolation="nearest")
    for value, (_, colour) in LABELS.items():
        if (msk == value).any():
            ax.contour(msk == value, levels=[0.5], colors=colour, linewidths=0.8)
    ax.set_title(title, fontsize=8)
    ax.axis("off")


def four_views(vol, spacing, msk, title: str, label: int, centred: bool, out: Path, dpi) -> None:  # type: ignore[no-untyped-def]
    """Axial, axial zoom, coronal and sagittal through the largest slice of `label`."""
    sx, sy, sz = spacing
    z, y, x = focus(msk, label)
    fig, axes = plt.subplots(1, 4, figsize=(15, 4.2))
    show(axes[0], vol[z], msk[z], title=f"axial, slice {z + 1}/{vol.shape[0]}")
    ys, xs = zoom_box(msk[z], margin=25)
    show(axes[1], vol[z][ys, xs], msk[z][ys, xs], title="axial zoom")
    # coronal and sagittal: flip z so superior is at the top; aspect = physical proportions
    show(axes[2], vol[::-1, y, :], msk[::-1, y, :], aspect=sz / sx, title="coronal")
    show(axes[3], vol[::-1, :, x], msk[::-1, :, x], aspect=sz / sy, title="sagittal")
    if centred:
        title += " | centred on the " + {2: "tumour", 3: "cyst"}[label]
    fig.suptitle(title, fontsize=9)
    handles = [plt.Line2D([], [], color=c, label=n) for _, (n, c) in LABELS.items()]
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=8, frameon=False)
    fig.tight_layout(rect=(0, 0.05, 1, 0.95))
    fig.savefig(out, dpi=dpi)
    plt.close(fig)


def render_kits23(kits_dir: Path, out_dir: Path, dpi) -> list[Path]:  # type: ignore[no-untyped-def]
    done = []
    for case, centre in KITS23:
        msk, _ = load(kits_dir / "segmentations" / f"{case}.nii.gz", lps=True)
        vol, spacing = load(kits_dir / "images" / f"{case}.nii.gz", lps=True)
        sx, sy, sz = spacing
        title = f"KiTS23 {case} | {sx:.2f}×{sy:.2f}×{sz:.2f} mm | reference labels"
        name = case if centre == "tumour" else f"{case}_{centre}"
        out = out_dir / "kits23" / f"{name}.png"
        four_views(vol, spacing, msk, title, FOCUS[centre], True, out, dpi)
        done.append(out)
    return done


def render_rmac(rmac_dir: Path, out_dir: Path, dpi) -> list[Path]:  # type: ignore[no-untyped-def]
    done = []
    for exam, phases in RMAC.items():
        msk, _ = load(rmac_dir / "masks" / exam / "mask_RMaC.nii.gz")
        z, _, _ = focus(msk, FOCUS["tumour"])
        fig, axes = plt.subplots(1, len(phases), figsize=(3.8 * len(phases), 4.2), squeeze=False)
        ys, xs = zoom_box(msk[z], margin=40)
        for ax, phase in zip(axes[0], phases, strict=True):
            vol, _ = load(rmac_dir / "volumes" / exam / f"{RMAC_FILE[phase]}.nii.gz")
            show(ax, vol[z][ys, xs], msk[z][ys, xs], title=f"{phase} (registered)")
        fig.suptitle(
            f"RMaC exam {exam} | slice {z + 1}/{msk.shape[0]} | mask drawn on the non-contrast grid",
            fontsize=9,
        )
        fig.tight_layout(rect=(0, 0, 1, 0.93))
        out = out_dir / "rmac" / f"{exam}.png"
        fig.savefig(out, dpi=dpi)
        plt.close(fig)
        done.append(out)
    return done


def render_tcga(ct_dir: Path, mask_dirs: dict[str, Path], out_dir: Path, dpi) -> list[Path]:  # type: ignore[no-untyped-def]
    done = []
    for c in TCGA:
        vol, spacing = load(ct_dir / c.patient / f"{c.series}.nii.gz")
        msk, _ = load(mask_dirs[c.mask] / c.patient / f"{c.series}_{c.mask}.nii.gz")
        sx, sy, sz = spacing
        title = (
            f"TCGA {c.patient} | {c.phase} ({c.phase_source}) | {c.manufacturer} | "
            f"{sx:.2f}×{sy:.2f}×{sz:.1f} mm | mask: {c.mask}"
        )
        name = c.patient if c.focus == "tumour" else f"{c.patient}_{c.focus}"
        out = out_dir / "tcga" / f"{name}.png"
        four_views(vol, spacing, msk, title, FOCUS[c.focus], c.centred_title, out, dpi)
        done.append(out)
    return done


# --- optional check against an existing figure set -------------------------------------------


def compare(outputs: list[Path], out_dir: Path, ref_dir: Path) -> bool:
    from PIL import Image

    same_all = True
    for out in outputs:
        rel = out.relative_to(out_dir)
        ref = ref_dir / rel
        if not ref.exists():
            print(f"{rel}: no reference file")
            same_all = False
            continue
        a, b = np.asarray(Image.open(out)), np.asarray(Image.open(ref))
        if a.shape != b.shape:
            print(f"{rel}: DIFFERENT size {a.shape[1]}x{a.shape[0]} vs {b.shape[1]}x{b.shape[0]}")
            same_all = False
        elif not np.array_equal(a, b):
            n = int((a != b).any(axis=-1).sum())
            print(f"{rel}: DIFFERENT, {n} of {a.shape[0] * a.shape[1]} pixels differ")
            same_all = False
        else:
            print(f"{rel}: pixel-identical ({a.shape[1]}x{a.shape[0]})")
    return same_all


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dataset", choices=("kits23", "rmac", "tcga", "all"), default="all")
    ap.add_argument("--kits23-dir", type=Path, help="KiTS23 folder with images/ and segmentations/")
    ap.add_argument("--rmac-dir", type=Path, help="processed RMaC folder with volumes/ and masks/")
    ap.add_argument("--tcga-ct-dir", type=Path, help="processed TCGA-KIRC CT volumes")
    ap.add_argument("--tcga-bamf-dir", type=Path, help="TCGA BAMF masks on the volumes' grids")
    ap.add_argument("--tcga-rccaid-dir", type=Path, help="TCGA RCC-AID masks on the volumes' grids")
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument(
        "--scale", type=float, default=2.0, help="2 = 2x the original size, 1 = original"
    )
    ap.add_argument("--compare-to", type=Path, help="existing figures to check against, read only")
    args = ap.parse_args()

    wanted = ("kits23", "rmac", "tcga") if args.dataset == "all" else (args.dataset,)
    needs = {
        "kits23": ["kits23_dir"],
        "rmac": ["rmac_dir"],
        "tcga": ["tcga_ct_dir", "tcga_bamf_dir", "tcga_rccaid_dir"],
    }
    missing = [
        f"--{a.replace('_', '-')}" for ds in wanted for a in needs[ds] if not getattr(args, a)
    ]
    if missing:
        ap.error("missing " + ", ".join(missing))
    dpi = BASE_DPI * args.scale
    dpi = int(dpi) if float(dpi).is_integer() else dpi

    for ds in wanted:
        (args.out_dir / ds).mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    with tempfile.TemporaryDirectory(prefix=".mplconfig-", dir=args.out_dir) as config_dir:
        setup_matplotlib(config_dir)
        if "kits23" in wanted:
            outputs += render_kits23(args.kits23_dir, args.out_dir, dpi)
        if "rmac" in wanted:
            outputs += render_rmac(args.rmac_dir, args.out_dir, dpi)
        if "tcga" in wanted:
            masks = {"BAMF": args.tcga_bamf_dir, "RCC-AID": args.tcga_rccaid_dir}
            outputs += render_tcga(args.tcga_ct_dir, masks, args.out_dir, dpi)
    for out in outputs:
        print("wrote", out)
    if args.compare_to:
        return 0 if compare(outputs, args.out_dir, args.compare_to) else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
