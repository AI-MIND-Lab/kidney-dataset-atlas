/**
 * Serialize data embedded in an HTML <script type="application/json"> block.
 * A literal "</script" closes the element even inside a JSON string, so the
 * characters that can enter HTML syntax are emitted as JSON unicode escapes.
 */
export function safeJson(value: unknown): string {
	return JSON.stringify(value)
		.replace(/</g, '\\u003c')
		.replace(/>/g, '\\u003e')
		.replace(/&/g, '\\u0026')
		.replace(/\u2028/g, '\\u2028')
		.replace(/\u2029/g, '\\u2029');
}
