import { spawnSync } from 'node:child_process';
import { createReadStream, existsSync, statSync } from 'node:fs';
import { createServer } from 'node:http';
import { dirname, extname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = resolve(fileURLToPath(new URL('../../', import.meta.url)));
const dist = join(projectRoot, 'dist');
const host = '127.0.0.1';
const port = 4321;
const basePath = '/kidney-dataset-atlas';
const npmCli =
	process.env.npm_execpath ?? join(dirname(process.execPath), 'node_modules', 'npm', 'bin', 'npm-cli.js');

const MIME = {
	'.css': 'text/css; charset=utf-8',
	'.csv': 'text/csv; charset=utf-8',
	'.html': 'text/html; charset=utf-8',
	'.js': 'text/javascript; charset=utf-8',
	'.json': 'application/json; charset=utf-8',
	'.svg': 'image/svg+xml',
	'.wasm': 'application/wasm',
};

export default async function globalSetup() {
	const build = spawnSync(process.execPath, [npmCli, 'run', 'build'], {
		cwd: projectRoot,
		stdio: 'inherit',
		env: {
			...process.env,
			ATLAS_FIXTURES: '1',
			SITE_URL: `http://${host}:${port}`,
			BASE_PATH: basePath,
		},
	});
	if (build.error) throw build.error;
	if (build.status !== 0) throw new Error(`Fixture build failed with exit code ${build.status}`);

	const server = createServer((request, response) => {
		let pathname;
		try {
			pathname = decodeURIComponent(new URL(request.url ?? '/', `http://${host}:${port}`).pathname);
		} catch {
			response.writeHead(400).end('Bad request');
			return;
		}
		if (pathname !== basePath && !pathname.startsWith(`${basePath}/`)) {
			response.writeHead(404).end('Not found');
			return;
		}

		const stripped = pathname.slice(basePath.length) || '/';
		let file = resolve(dist, stripped.replace(/^\/+/, ''));
		if (relative(dist, file).startsWith('..')) {
			response.writeHead(403).end('Forbidden');
			return;
		}
		if (stripped.endsWith('/') || (existsSync(file) && statSync(file).isDirectory())) file = join(file, 'index.html');
		if (!existsSync(file) || !statSync(file).isFile()) {
			response.writeHead(404).end('Not found');
			return;
		}

		response.writeHead(200, {
			'content-type': MIME[extname(file)] ?? 'application/octet-stream',
			'cache-control': 'no-store',
		});
		if (request.method === 'HEAD') response.end();
		else createReadStream(file).pipe(response);
	});

	await new Promise((resolveListen, reject) => {
		server.once('error', reject);
		server.listen(port, host, resolveListen);
	});

	return async () => {
		await new Promise((resolveClose, reject) => server.close((error) => (error ? reject(error) : resolveClose())));
	};
}
