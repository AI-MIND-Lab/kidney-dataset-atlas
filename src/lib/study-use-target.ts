interface TargetUse {
	release: string | null;
	externalCohort: { name: string } | null;
}

export interface ReleaseContext {
	datasetSlug: string;
	datasetName: string;
	releaseId: string;
	versionLabel: string;
}

/** External/private cohorts are labels only; only catalogued releases get routes. */
export function studyUseTarget(use: TargetUse, context?: ReleaseContext): { label: string; path: string | null } {
	if (use.externalCohort) return { label: use.externalCohort.name, path: null };
	if (context) {
		return {
			label: `${context.datasetName} — ${context.versionLabel}`,
			path: `/datasets/${context.datasetSlug}/releases/${context.releaseId}/`,
		};
	}
	return { label: use.release ?? 'Unknown cohort', path: null };
}
