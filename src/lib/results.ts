/**
 * A paper's reported results, one row per value.
 *
 * A result that covers several releases (for example a subtype classifier evaluated on three TCGA projects
 * together) is recorded once in each release's study use, so readers of each dataset page see it. On the paper
 * page it is shown once, with the list of releases it was recorded against.
 */

interface ResultLike {
	model: string;
	metric: string;
	value: number | null;
	units: string | null;
	confidenceInterval: string | null;
	subset: string | null;
	split: string | null;
	evaluation: string;
}

/** Two results are the same row when everything a reader sees about them is the same. */
export const resultKey = (r: ResultLike) =>
	JSON.stringify([r.model, r.metric, r.value, r.units, r.confidenceInterval, r.subset, r.split, r.evaluation]);

export function groupResults<U extends { results: ResultLike[] }>(
	uses: U[],
	modelOrder: string[] = [],
): { result: U['results'][number]; uses: U[] }[] {
	type R = U['results'][number];
	const grouped = new Map<string, { result: R; uses: U[] }>();
	for (const use of uses) {
		for (const result of use.results) {
			const key = resultKey(result);
			const entry = grouped.get(key) ?? { result, uses: [] as U[] };
			entry.uses.push(use);
			grouped.set(key, entry);
		}
	}
	const rank = (model: string) => {
		const i = modelOrder.indexOf(model);
		return i === -1 ? modelOrder.length : i;
	};
	// Stable sort: models in the given order, results in recorded order within a model.
	return [...grouped.values()].sort((a, b) => rank(a.result.model) - rank(b.result.model));
}
