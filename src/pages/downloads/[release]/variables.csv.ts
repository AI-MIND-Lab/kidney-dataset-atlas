import type { APIRoute, GetStaticPaths } from 'astro';
import { publishedReleases, variablesForRelease } from '../../../lib/catalog';
import { toCsv } from '../../../lib/csv';
import { DICTIONARY_HEADER, dictionaryRow } from '../../../lib/dictionary';

// Written as real files at build time, so a download works without JavaScript
// and can be linked to from anywhere.
export const getStaticPaths = (async () => {
	const releases = await publishedReleases();
	return releases.map((release) => ({ params: { release: release.data.id }, props: { release } }));
}) satisfies GetStaticPaths;

export const GET: APIRoute = ({ props }) => {
	const { release } = props as { release: Awaited<ReturnType<typeof publishedReleases>>[number] };
	const meta = {
		releaseId: release.data.id,
		completeness: release.data.dictionary.completeness,
		inspectedScope: release.data.dictionary.inspectedScope,
	};
	const rows = variablesForRelease(release.data.id).map((entry) => dictionaryRow(entry, meta));

	return new Response(toCsv(DICTIONARY_HEADER, rows), {
		headers: {
			'Content-Type': 'text/csv; charset=utf-8',
			'Content-Disposition': `attachment; filename="${release.data.id}-variables.csv"`,
		},
	});
};
