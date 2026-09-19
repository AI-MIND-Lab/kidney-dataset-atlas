/** Helpers that work on raw records, with no dependency on the content layer. */

/**
 * Source ids cited anywhere in a record, including inside nested evidence
 * objects, in the order they are met. A page can then list exactly the sources
 * behind what it shows.
 */
export function collectSourceIds(value: unknown, found = new Set<string>()): string[] {
	if (!value || typeof value !== 'object') return [...found];
	if (Array.isArray(value)) {
		for (const item of value) collectSourceIds(item, found);
		return [...found];
	}
	for (const [key, item] of Object.entries(value)) {
		if (key === 'sources' && Array.isArray(item)) {
			for (const id of item) if (typeof id === 'string') found.add(id);
			continue;
		}
		collectSourceIds(item, found);
	}
	return [...found];
}
