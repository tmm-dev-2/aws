import type { NextApiRequest, NextApiResponse } from 'next';
import { spawn } from 'child_process';
import path from 'path';

export default async function handler(
	req: NextApiRequest,
	res: NextApiResponse
) {
	if (req.method !== 'GET') {
		return res.status(405).json({ message: 'Method not allowed' });
	}

	const { symbol, timeframe } = req.query;

	if (!symbol || !timeframe) {
		return res.status(400).json({ message: 'Missing required parameters' });
	}

	try {
		const pythonProcess = spawn('python', [
			path.join(process.cwd(), 'strategies', 'rolling-vwap-kosine-p1', 'rolling-vwap-kosine-p1.py'),
			symbol as string,
			timeframe as string
		]);

		let result = '';

		pythonProcess.stdout.on('data', (data) => {
			result += data.toString();
		});

		pythonProcess.stderr.on('data', (data) => {
			console.error(`Python Error: ${data}`);
		});

		return new Promise((resolve, reject) => {
			pythonProcess.on('close', (code) => {
				if (code !== 0) {
					reject(res.status(500).json({ message: 'Error executing Python script' }));
					return;
				}
				try {
					const jsonResult = JSON.parse(result);
					resolve(res.status(200).json(jsonResult));
				} catch (error) {
					reject(res.status(500).json({ message: 'Error parsing Python result' }));
				}
			});
		});
	} catch (error) {
		console.error('API Error:', error);
		return res.status(500).json({ message: 'Internal server error' });
	}
}