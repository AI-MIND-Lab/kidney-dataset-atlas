/**
 * Record schemas for the Kidney Dataset Atlas.
 *
 * These are the single source of truth: `src/content.config.ts` uses them to
 * type the content collections, and `scripts/validate.mjs` uses them to check
 * the files on disk before a build. Plain JavaScript so both can import them.
 */
import { z } from 'astro/zod';

/** Stable machine identifiers and route slugs use one conservative format. */
export const recordId = z
	.string()
	.regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/, 'Use lowercase letters, numbers, and single hyphens only');
export const routeSlug = recordId;

/** Explicit state for anything that is not a plain yes. */
export const STATE = ['present', 'absent', 'not_documented', 'not_verified', 'not_applicable'];
export const state = z.enum(STATE);

/** A checked claim points at the sources it came from. */
export const evidence = z.object({
	sources: z.array(z.string()).default([]),
	locator: z.string().optional(),
	status: z.enum(['verified', 'not_verified']).default('not_verified'),
	verifiedOn: z.coerce.date().nullable().default(null),
	note: z.string().optional(),
});

/**
 * Counts are never guessed. An unknown count is null plus a state, never zero,
 * and each unit is counted separately.
 */
export const count = z
	.object({
		value: z.number().int().nonnegative().nullable(),
		status: state,
		evidence: evidence.optional(),
	})
	.superRefine((entry, context) => {
		if (entry.status === 'present' && entry.value === null) {
			context.addIssue({
				code: 'custom',
				path: ['value'],
				message: 'A present count requires a numeric value',
			});
		}
		if (entry.status !== 'present' && entry.value !== null) {
			context.addIssue({
				code: 'custom',
				path: ['value'],
				message: 'An absent, unknown, or not-applicable count must use null',
			});
		}
	});

/**
 * Units are counted separately and never added together. Images and patches
 * matter for collections distributed as pictures rather than as studies: a
 * count of images is not a count of patients.
 */
const countsByUnit = z.object({
	patients: count.optional(),
	examinations: count.optional(),
	lesions: count.optional(),
	slices: count.optional(),
	slides: count.optional(),
	images: count.optional(),
	patches: count.optional(),
	records: count.optional(),
});

/** One of the five eligibility gates from the brief (docs/brief.md, section 2). */
const eligibilityCheck = z.object({
	status: z.enum(['pass', 'fail', 'unknown']),
	note: z.string().optional(),
	evidence: evidence.optional(),
});

const eligibility = z.object({
	publicAccess: eligibilityCheck,
	deidentification: eligibilityCheck,
	noPhiHosted: eligibilityCheck,
	termsPermitUse: eligibilityCheck,
	samplePermission: eligibilityCheck,
});

/** A single documented fact: what the provider says, plus where it says it. */
export const feature = z.object({
	status: state,
	note: z.string().optional(),
	evidence: evidence.optional(),
});

export const MODALITIES = ['ct', 'mri', 'ultrasound', 'pathology', 'clinical_table', 'molecular', 'other'];
export const DISEASES = [
	'renal_tumor',
	'ckd',
	'aki',
	'stones',
	'cysts',
	'transplantation',
	'dialysis',
	'outcomes',
	'other',
];
export const TASKS = [
	'segmentation',
	'classification',
	'detection',
	'regression',
	'survival',
	'registration',
	'report_generation',
	'other',
];
/**
 * How the data are obtained. `not_documented` is for a collection whose
 * download conditions could not be established: guessing between open and
 * restricted would put a wrong badge on a dataset page.
 */
export const ACCESS_MODES = [
	'direct_open_download',
	'public_account_or_terms',
	'registration_gated',
	'application_or_manual_approval',
	'controlled_data_use_agreement',
	'partial_or_sample_release',
	'private_institutional',
	'access_unclear',
];

/** Whose tissue this is. Nonhuman and synthetic material is never left implied. */
export const SPECIES = ['human', 'mouse', 'rat', 'pig', 'other_nonhuman', 'mixed', 'synthetic', 'not_documented'];

/** Who or what produced the annotations, which is not the same as their quality. */
export const ANNOTATION_PROVENANCE = [
	'expert',
	'trainee',
	'crowd',
	'model_generated',
	'mixed',
	'none',
	'not_documented',
];
export const ANNOTATIONS = [
	'segmentation_masks',
	'bounding_boxes',
	'classification_labels',
	'pathology_labels',
	'outcome_labels',
	'none',
	'not_documented',
];

export const dataset = z.object({
	id: recordId,
	slug: routeSlug,
	name: z.string(),
	aliases: z.array(z.string()).default([]),
	summary: z.string(),
	diseaseTags: z.array(z.enum(DISEASES)).default([]),
	species: z.enum(SPECIES),
	officialUrl: z.url(),
	/** The dataset's own DOI, which is never the same field as a paper's DOI. */
	doi: z.string().nullable().default(null),
	sources: z.array(z.string()).default([]),
});

export const release = z.object({
	id: recordId,
	dataset: recordId,
	versionLabel: z.string(),
	/** Exactly one published release per dataset is the current canonical page. */
	current: z.boolean().default(false),
	releaseDate: z.coerce.date().nullable().default(null),
	counts: countsByUnit.default({}),
	modalities: z.array(z.enum(MODALITIES)).default([]),
	cohort: z.string().optional(),
	tasks: z.array(z.enum(TASKS)).default([]),
	/** What is labelled, as documented by the provider. Empty means not documented. */
	annotations: z.array(z.enum(ANNOTATIONS)).default([]),
	/** Who produced those labels: an expert, a crowd, or a model. */
	annotationProvenance: z
		.object({
			kind: z.enum(ANNOTATION_PROVENANCE),
			note: z.string().optional(),
			evidence: evidence.optional(),
		})
		.optional(),
	/** A release-specific dataset DOI, such as an archived version. */
	doi: z.string().nullable().default(null),
	access: z.object({
		mode: z.enum(ACCESS_MODES),
		registrationVisible: z.boolean().default(false),
		instructions: z.string(),
		evidence: evidence.optional(),
	}),
	license: z.object({
		name: z.string(),
		url: z.url().optional(),
		conditions: z.string().optional(),
	}),
	deidentification: z.object({
		// "Provider documents de-identification", with a source. Never "HIPAA-free".
		statement: z.string(),
		status: state,
		evidence: evidence.optional(),
	}),
	pairing: z
		.array(
			z.object({
				kind: z.enum(['same_patient', 'same_lesion', 'same_session_phases', 'follow_up']),
				modalities: z.array(z.enum(MODALITIES)).default([]),
				status: state,
				note: z.string().optional(),
				evidence: evidence.optional(),
			}),
		)
		.default([]),
	dictionary: z.object({
		completeness: z.enum(['complete_for_inspected_release', 'partial', 'documentation_only']),
		inspectedScope: z.string(),
	}),
		/**
	 * Facts the comparison asks about directly. Each is stated, never inferred:
	 * pathology labels do not prove whole-slide images exist, and a CT modality
	 * does not prove which phases were acquired.
	 */
	features: z
		.object({
			wsi: feature.optional(),
			ctPhases: feature.extend({ phases: z.array(z.string()).default([]) }).optional(),
			clinicalData: feature.optional(),
			followUp: feature.optional(),
		})
		.default({}),
	/** Files, formats, identifiers, joins and observation levels, in prose. */
	structure: z.string().optional(),
	/** Release-specific research context, kept separate from the dataset-family overview. */
	notes: z.array(z.object({ title: z.string(), text: z.string(), evidence: evidence })).default([]),
	citation: z.string().optional(),
	limitations: z.array(z.string()).default([]),
	eligibility,
	catalogStatus: z.enum(['draft', 'published']).default('draft'),
	verifiedOn: z.coerce.date().nullable().default(null),
	researchedBy: z.string(),
	approvedBy: z.string().nullable().default(null),
	approvedOn: z.coerce.date().nullable().default(null),
	sources: z.array(z.string()).default([]),
});

export const variable = z.object({
	id: recordId,
	release: recordId,
	originalName: z.string(),
	file: z.string().optional(),
	definition: z.string(),
	type: z.enum(['integer', 'decimal', 'categorical', 'boolean', 'date', 'text', 'image', 'other']),
	unit: z.string().nullable().default(null),
	coding: z.array(z.object({ code: z.string(), meaning: z.string() })).default([]),
	missingValues: z.array(z.string()).default([]),
	observationLevel: z.enum(['patient', 'examination', 'lesion', 'slice', 'slide', 'record']),
	timePoint: z.string().nullable().default(null),
	role: z.enum(['identifier', 'predictor', 'outcome', 'descriptor', 'annotation', 'other']),
	group: z.enum(['clinical', 'imaging', 'pathology', 'outcome', 'administrative', 'other']),
	derivation: z.enum(['raw', 'derived']),
	normalizedConcept: z.string().nullable().default(null),
	provenance: z.string().optional(),
	evidence: evidence.optional(),
});

const modelField = z.object({ status: state, url: z.url().optional(), note: z.string().optional() });

/** One step of a model, as drawn in the atlas's own pipeline diagram. */
const pipelineStep = z.object({ label: z.string(), detail: z.string().optional() });

export const model = z.object({
	id: recordId,
	name: z.string(),
	role: z.enum(['proposed', 'variant', 'baseline']),
	originalPaper: z.string().nullable().default(null),
	task: z.enum(TASKS),
	/**
	 * The model as a left-to-right pipeline, from input to output. The atlas
	 * draws its own diagram from these steps, so every model has a picture even
	 * when the paper's figure may not be reproduced.
	 */
	pipeline: z.array(pipelineStep).default([]),
	backbone: z.string().optional(),
	inputRepresentation: z.enum(['2d', '2.5d', '3d', 'wsi', 'patch', 'tabular', 'multimodal', 'other']).optional(),
	preprocessing: z.string().optional(),
	fusion: z.string().optional(),
	loss: z.string().optional(),
	outputs: z.string().optional(),
	trainingInputs: z.string().optional(),
	inferenceInputs: z.string().optional(),
	code: modelField.optional(),
	weights: modelField.optional(),
	/** Where in the paper the architecture facts were read, so a reviewer can check each row. */
	evidence: evidence.optional(),
});

/**
 * Licences under which a paper's figure may be copied onto the site, with
 * attribution. A figure under any other licence is linked, never reproduced.
 */
export const REUSABLE_FIGURE_LICENSES = [
	'https://creativecommons.org/licenses/by/4.0/',
	'https://creativecommons.org/licenses/by/3.0/',
	'https://creativecommons.org/publicdomain/zero/1.0/',
];

/** A figure copied from a paper, shown with the paper's caption and a full credit line. */
export const paperFigure = z.object({
	id: recordId,
	/** The paper's own figure number, e.g. "Figure 1". */
	label: z.string(),
	title: z.string(),
	/** A file under public/figures/<paper id>/. */
	path: z.string().regex(/^\/figures\/[a-z0-9-]+\/[a-z0-9-]+\.(webp|png|jpg|svg)$/, 'Store figures in public/figures/<paper id>/'),
	width: z.number().int().positive(),
	height: z.number().int().positive(),
	alt: z.string(),
	/** Quoted from the paper, unchanged. */
	caption: z.string(),
	/** How the parts of the figure correspond to the model table, in the atlas's words. */
	mapsTo: z.string().optional(),
	/** Authors, title, venue, year, figure number and copyright holder. */
	credit: z.string(),
	license: z.object({
		name: z.string(),
		url: z.string().refine((url) => REUSABLE_FIGURE_LICENSES.includes(url), {
			message: `A reproduced figure needs a reusable licence: ${REUSABLE_FIGURE_LICENSES.join(', ')}`,
		}),
	}),
	/** What was changed, as the licence requires; "None" is a valid answer. */
	changes: z.string(),
	/** Where the image file was taken from. */
	source: z.url(),
});

/** A figure the site may not copy: named, summarised in the atlas's words, and linked. */
export const linkedFigure = z.object({
	label: z.string(),
	title: z.string(),
	url: z.url(),
	summary: z.string(),
	reason: z.string(),
});

export const paper = z.object({
	id: recordId,
	slug: routeSlug,
	title: z.string(),
	authors: z.array(z.string()).default([]),
	year: z.number().int().nullable().default(null),
	venue: z.string().nullable().default(null),
	publicationStatus: z.enum(['preprint', 'peer_reviewed', 'not_documented']),
	doi: z.string().nullable().default(null),
	url: z.url().nullable().default(null),
	methodSummary: z.string().optional(),
	figures: z.array(paperFigure).default([]),
	linkedFigures: z.array(linkedFigure).default([]),
	models: z.array(model).default([]),
	catalogStatus: z.enum(['draft', 'published']).default('draft'),
	approvedBy: z.string().nullable().default(null),
	approvedOn: z.coerce.date().nullable().default(null),
	sources: z.array(z.string()).default([]),
});

export const studyUse = z
	.object({
		id: recordId,
		paper: recordId,
		release: recordId.nullable().default(null),
		externalCohort: z
			.object({
				name: z.string(),
				accessMode: z.enum(ACCESS_MODES),
				note: z.string().optional(),
				evidence,
			})
			.nullable()
			.default(null),
		/**
		 * What the paper is to this release:
		 * - original: the release's own publication
		 * - benchmark: the dataset's own paper or challenge report, which evaluates
		 *   methods on it — real computer-vision use, but not independent adoption
		 * - downstream: a separate study that used the data
		 * - descriptor: a publication that describes the dataset without experiments
		 */
		role: z.enum(['original', 'benchmark', 'downstream', 'descriptor']),
		// A paper mentioning a dataset is not evidence that it used it.
		actualUseEvidence: evidence,
		subset: z.string().nullable().default(null),
		preprocessing: z.string().nullable().default(null),
		task: z.enum(TASKS).nullable().default(null),
		trainTestRole: z.enum(['train', 'test', 'train_and_test', 'validation', 'not_documented']),
		split: z.string().nullable().default(null),
		results: z
			.array(
				z.object({
					model: z.string(),
					metric: z.string(),
					value: z.number().nullable(),
					units: z.string().nullable().default(null),
					confidenceInterval: z.string().nullable().default(null),
					subset: z.string().nullable().default(null),
					split: z.string().nullable().default(null),
					patientLevelHandling: z.string().nullable().default(null),
					evaluation: z.enum(['internal', 'external', 'not_documented']),
					evidence: evidence.optional(),
				}),
			)
			.default([]),
	})
	.superRefine((entry, context) => {
		if (Boolean(entry.release) === Boolean(entry.externalCohort)) {
			context.addIssue({
				code: 'custom',
				path: ['release'],
				message: 'Name exactly one target: a catalogued release or an external cohort',
			});
		}
	});

export const sample = z.object({
	id: recordId,
	release: recordId,
	kind: z.enum(['dataset_sample', 'published_figure']),
	assets: z
		.array(
			z.object({
				path: z.string(),
				role: z.enum(['image', 'mask', 'overlay']),
				sliceIndex: z.number().int().nullable().default(null),
				width: z.number().int().positive(),
				height: z.number().int().positive(),
			}),
		)
		.min(1),
	caption: z.string(),
	alt: z.string(),
	attribution: z.string(),
	reuseTerms: z.string(),
	permissionApprovedBy: z.string().nullable().default(null),
	permissionApprovedOn: z.coerce.date().nullable().default(null),
	alignment: z.string().optional(),
	sources: z.array(z.string()).default([]),
});

export const qualityFinding = z.object({
	id: recordId,
	release: recordId,
	category: z.enum(['observed_issue', 'published_report', 'potential_check']),
	description: z.string(),
	inspectedScope: z.string(),
	affected: count.optional(),
	detection: z.string().optional(),
	impact: z.string().optional(),
	handling: z.string().optional(),
	sources: z.array(z.string()).default([]),
});

export const source = z.object({
	id: recordId,
	url: z.url(),
	title: z.string(),
	locator: z.string().optional(),
	accessedOn: z.coerce.date(),
});

/**
 * How one release relates to another: a subset, a derived annotation set, a
 * later version, or an aggregation. The other side may be a release in this
 * catalog or, when it is not catalogued, a named external collection — so a
 * derived annotation set can say what it was derived from either way.
 */
export const relation = z.object({
	id: recordId,
	from: recordId,
	to: recordId.nullable().default(null),
	toExternal: z
		.object({ name: z.string(), url: z.url().optional() })
		.nullable()
		.default(null),
	type: z.enum(['subset_of', 'derived_from', 'version_of', 'aggregates', 'annotates']),
	explanation: z.string(),
	evidence: evidence.optional(),
	sources: z.array(z.string()).default([]),
});

export const overlap = z.object({
	id: recordId,
	releases: z.array(recordId).min(2),
	type: z.enum(['same_cohort', 'partial_cohort', 'superset', 'unknown']),
	count: count.optional(),
	explanation: z.string(),
	evidence: evidence.optional(),
});

/** Collections keyed by the directory they live in. */
export const schemas = {
	datasets: dataset,
	releases: release,
	papers: paper,
	variables: variable,
	'study-uses': studyUse,
	samples: sample,
	quality: qualityFinding,
	sources: source,
	overlap: overlap,
	relations: relation,
};
