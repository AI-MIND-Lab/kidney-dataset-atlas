import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import { safeJson } from '../src/lib/safe-json.ts';

test('embedded JSON escapes script terminators and HTML-significant characters', () => {
	const payload = {
		name: '</script><script>globalThis.pwned=true</script>',
		query: '<img src=x onerror=alert(1)> & \u2028 \u2029',
	};
	const serialized = safeJson(payload);
	assert.equal(serialized.includes('</script>'), false);
	assert.equal(serialized.includes('<'), false);
	assert.equal(serialized.includes('>'), false);
	assert.deepEqual(JSON.parse(serialized), payload);
});
