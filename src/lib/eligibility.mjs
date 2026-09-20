/**
 * The five gates a release must pass before it can be published.
 *
 * Shared by the validator and the pages, so the checklist a curator reads in
 * the terminal and the one a reader sees on a draft page are the same list.
 */
export const ELIGIBILITY_LABELS = {
	publicAccess: 'Publicly accessible without an approval committee',
	deidentification: 'Provider documents de-identification',
	noPhiHosted: 'No patient records hosted by this site',
	termsPermitUse: "Provider's terms permit this use",
	samplePermission: 'Reuse permission checked for every displayed sample',
};

export const ELIGIBILITY_KEYS = Object.keys(ELIGIBILITY_LABELS);

/** The checks that are not yet a pass, in the order they are listed. */
export function unresolvedChecks(eligibility) {
	return ELIGIBILITY_KEYS.filter((key) => eligibility?.[key]?.status !== 'pass').map((key) => ({
		key,
		label: ELIGIBILITY_LABELS[key],
		status: eligibility?.[key]?.status ?? 'unknown',
		note: eligibility?.[key]?.note ?? null,
	}));
}
