import { expect, test } from '@playwright/test';

test('explorer to dataset, paper, search, comparison, and CSV export', async ({ page }) => {
	await page.goto('./');
	await expect(page.getByRole('heading', { name: 'Kidney Dataset Atlas' })).toBeVisible();

	const explorerSearch = page.getByLabel('Search datasets');
	await explorerSearch.fill('renal ct');
	await expect(page).toHaveURL(/\?q=renal\+ct$/);
	await expect(page.locator('[data-count]')).toHaveText('1 dataset of 3');
	await page.getByRole('link', { name: 'Fixture Renal CT Collection (synthetic)' }).first().click();

	await expect(page.getByRole('heading', { level: 1, name: 'Fixture Renal CT Collection (synthetic)' })).toBeVisible();
	await page.getByRole('link', { name: 'Data dictionary' }).click();
	await expect(page.getByRole('heading', { level: 2, name: 'Data dictionary' })).toBeVisible();
	await expect(page.getByText('case_id', { exact: true })).toBeVisible();

	await page.getByRole('link', { name: 'A synthetic paper about a synthetic dataset' }).click();
	await expect(page.getByRole('heading', { level: 1, name: 'A synthetic paper about a synthetic dataset' })).toBeVisible();
	await expect(page.getByRole('columnheader', { name: 'Release or cohort' }).first()).toBeVisible();
	// Results: one row per value, with the split and any patient-level handling shown together.
	await expect(page.getByRole('heading', { level: 2, name: 'Reported results' })).toBeVisible();
	await expect(page.getByRole('columnheader', { name: 'Evaluated on' })).toBeVisible();
	await expect(page.getByRole('columnheader', { name: 'Split', exact: true }).first()).toBeVisible();
	await expect(page.getByText('Invented patient-level split').first()).toBeVisible();
	await expect(page.getByText('Fixture private hospital cohort')).toBeVisible();
	await expect(page.getByText('Fixture private hospital cohort').locator('a')).toHaveCount(0);

	await page.locator('.site-search input').fill('FixtureNet');
	await page.locator('.site-search input').press('Enter');
	await expect(page).toHaveURL(/\/search\/\?q=FixtureNet$/);
	await expect(page.locator('[data-search-status]')).toContainText(/result/);
	await expect(page.locator('[data-search-results]')).toContainText('A synthetic paper about a synthetic dataset');

	await page.getByRole('navigation', { name: 'Primary' }).getByRole('link', { name: 'Compare' }).click();
	await page.getByRole('checkbox', { name: /Fixture Renal CT Collection.*v2/ }).check();
	await page.getByRole('checkbox', { name: /Fixture Pathology Slide Set/ }).check();
	await expect(page.locator('[data-compare-table]')).toBeVisible();
	await expect(page.locator('.compare-table')).toContainText('Fixture Renal CT Collection');

	const downloadPromise = page.waitForEvent('download');
	await page.getByRole('button', { name: 'Download CSV' }).click();
	const download = await downloadPromise;
	expect(download.suggestedFilename()).toMatch(/^comparison-.*\.csv$/);
});
