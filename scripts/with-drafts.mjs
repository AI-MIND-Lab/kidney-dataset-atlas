#!/usr/bin/env node
/**
 * Builds and serves the site including records that are still drafts, so a
 * curator can read them as pages before approving them. Every page in this
 * build is marked, and scripts/check-output.mjs refuses a build carrying that
 * mark unless ATLAS_DRAFTS is set. Nothing here publishes anything.
 */
import { spawn } from 'node:child_process';

const args = process.argv.slice(2);
const script = args.length > 0 ? args : ['run', 'preview:site'];

const child = spawn('npm', script, {
	stdio: 'inherit',
	shell: process.platform === 'win32',
	env: { ...process.env, ATLAS_DRAFTS: '1' },
});

child.on('exit', (code) => process.exit(code ?? 0));
