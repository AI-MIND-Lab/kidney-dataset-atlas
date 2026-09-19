/**
 * Record schemas for the Kidney Dataset Atlas.
 *
 * These are the single source of truth: `src/content.config.ts` uses them to
 * type the content collections, and `scripts/validate.mjs` uses them to check
 * the files on disk before a build. Plain JavaScript so both can import them.
 */
import { z } from 'astro/zod';

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
export const count = z.object({
	value: z.number().int().nonnegative().nullable(),
	status: state,
	evidence: evidence.optional(),
});

const countsByUnit = z.object({
	patients: count.optional(),
	examinations: count.optional(),
	lesions: count.optional(),
	slices: count.optional(),
	slides: count.optional(),
	records: count.optional(),
});

/** One of the five eligibility gates from the brief. */
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
export const ACCESS_MODES = ['open_download', 'registration_required', 'restricted'];
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
	id: z.string(),
	slug: z.string(),
	name: z.string(),
	aliases: z.array(z.string()).default([]),
	summary: z.string(),
	diseaseTags: z.array(z.enum(DISEASES)).default([]),
	officialUrl: z.url(),
	sources: z.array(z.string()).default([]),
});

export const release = z.object({
	id: z.string(),
	dataset: z.string(),
	versionLabel: z.string(),
	releaseDate: z.coerce.date().nullable().default(null),
	counts: countsByUnit.default({}),
	modalities: z.array(z.enum(MODALITIES)).default([]),
	cohort: z.string().optional(),
	tasks: z.array(z.enum(TASKS)).default([]),
	/** What is labelled, as documented by the provider. Empty means not documented. */
	annotations: z.array(z.enum(ANNOTATIONS)).default([]),
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
	id: z.string(),
	release: z.string(),
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

export const model = z.object({
	id: z.string(),
	name: z.string(),
	role: z.enum(['proposed', 'variant', 'baseline']),
	originalPaper: z.string().nullable().default(null),
	task: z.enum(TASKS),
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
});

export const paper = z.object({
	id: z.string(),
	slug: z.string(),
	title: z.string(),
	authors: z.array(z.string()).default([]),
	year: z.number().int().nullable().default(null),
	venue: z.string().nullable().default(null),
	publicationStatus: z.enum(['preprint', 'peer_reviewed', 'not_documented']),
	doi: z.string().nullable().default(null),
	url: z.url().nullable().default(null),
	methodSummary: z.string().optional(),
	models: z.array(model).default([]),
	catalogStatus: z.enum(['draft', 'published']).default('draft'),
	sources: z.array(z.string()).default([]),
});

export const studyUse = z.object({
	id: z.string(),
	paper: z.string(),
	release: z.string(),
	role: z.enum(['original', 'downstream']),
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
});

export const sample = z.object({
	id: z.string(),
	release: z.string(),
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
	id: z.string(),
	release: z.string(),
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
	id: z.string(),
	url: z.url(),
	title: z.string(),
	locator: z.string().optional(),
	accessedOn: z.coerce.date(),
});

export const overlap = z.object({
	id: z.string(),
	releases: z.array(z.string()).min(2),
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
};
