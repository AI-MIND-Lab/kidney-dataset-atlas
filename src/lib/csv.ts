/**
 * CSV writing for the dictionary and comparison exports.
 *
 * Two things matter here. Quoting, so a definition containing a comma or a
 * line break survives the trip; and formula guarding, because a spreadsheet
 * treats a cell beginning with = + - @ as a formula, and dataset records
 * contain text this site did not write.
 */

const FORMULA_START = /^[=+\-@\t\r]/;
const NUMERIC = /^-?\d+(\.\d+)?$/;

/** A negative number is a number; anything else a spreadsheet might execute is text. */
export function guardFormula(value: string): string {
	if (FORMULA_START.test(value) && !NUMERIC.test(value)) return `'${value}`;
	return value;
}

export function escapeField(value: string | number | null | undefined): string {
	if (value === null || value === undefined) return '';
	if (typeof value === 'number') return String(value);
	const guarded = guardFormula(value);
	if (/[",\r\n]/.test(guarded) || guarded !== guarded.trim()) {
		return `"${guarded.replace(/"/g, '""')}"`;
	}
	return guarded;
}

export type CsvRow = (string | number | null | undefined)[];

export function toCsv(header: string[], rows: CsvRow[]): string {
	return [header, ...rows].map((row) => row.map(escapeField).join(',')).join('\r\n');
}
