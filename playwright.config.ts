import { defineConfig } from '@playwright/test';

const basePath = '/kidney-dataset-atlas';
const origin = 'http://127.0.0.1:4321';

export default defineConfig({
	testDir: './tests/browser',
	globalSetup: './tests/browser/global-setup.mjs',
	fullyParallel: false,
	workers: 1,
	reporter: process.env.CI ? 'github' : 'list',
	use: {
		baseURL: `${origin}${basePath}/`,
		trace: 'retain-on-failure',
	},
});
