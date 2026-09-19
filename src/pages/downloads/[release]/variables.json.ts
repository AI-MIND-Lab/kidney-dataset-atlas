import type { APIRoute, GetStaticPaths } from 'astro';
import { publishedReleases, sourcesFor, variablesForRelease } from '../../../lib/catalog';

export const getStaticPaths = (async () => {
	const releases = await publishedReleases();
	return releases.map((release) => ({ params: { release: release.data.id }, props: { release } }));
}) satisfies GetStaticPaths;

export const GET: APIRoute = ({ props }) => {
	const { release } = props as { release: Awaited<ReturnType<typeof publishedReleases>>[number] };
	const variables = variablesForRelease(release.data.id);

	// The export says what it is: which release, how complete the dictionary
	// is, what was inspected, and the sources behind the variables.
	const payload = {
		release: release.data.id,
		dataset: release.data.dataset,
		versionLabel: release.data.versionLabel,
		dictionary: release.data.dictionary,
		verifiedOn: release.data.verifiedOn,
		variableCount: variables.length,
		sources: sourcesFor(variables),
		variables,
	};

	return new Response(JSON.stringify(payload, null, '\t'), {
		headers: {
			'Content-Type': 'application/json; charset=utf-8',
			'Content-Disposition': `attachment; filename="${release.data.id}-variables.json"`,
		},
	});
};
