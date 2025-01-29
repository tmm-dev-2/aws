import type { NextApiRequest, NextApiResponse } from 'next';
import { spawn } from 'child_process';
import path from 'path';

const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:5000';
const USE_EXTERNAL_API = process.env.USE_EXTERNAL_API === 'true';

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
		if (USE_EXTERNAL_API) {
			const response = await fetch(`${PYTHON_API_URL}/calculate_kernel_regression`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ symbol, timeframe }),
			});

			if (!response.ok) {
				throw new Error('Failed to fetch from Python API');
			}

			const data = await response.json();
			return res.status(200).json(data);
		} else {
			const pythonProcess = spawn('python', [
				path.join(process.cwd(), 'strategies', 'kernel-regression-p2', 'kernel-regression-p2.py'),
				symbol as string,
				timeframe as string
			]);

			let result = '';

			pythonProcess.stdout.on('data', (data) => {
				result += data.toString();
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
		}
	} catch (error) {
		console.error('API Error:', error);
		return res.status(500).json({ message: 'Internal server error' });
	}
}