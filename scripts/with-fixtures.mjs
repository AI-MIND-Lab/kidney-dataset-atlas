#!/usr/bin/env node
/**
 * Runs an Astro command against the synthetic fixtures instead of the real
 * catalog, so the interface can be developed before records are approved.
 * Usage: node scripts/with-fixtures.mjs dev
 */
import { spawn } from 'node:child_process';

const args = process.argv.slice(2);
if (args.length === 0) {
	console.error('usage: node scripts/with-fixtures.mjs <astro command> [...args]');
	process.exit(1);
}

const child = spawn('npx', ['astro', ...args], {
	stdio: 'inherit',
	shell: process.platform === 'win32',
	env: { ...process.env, ATLAS_FIXTURES: '1' },
});

child.on('exit', (code) => process.exit(code ?? 0));
