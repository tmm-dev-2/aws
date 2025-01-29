import type { NextApiRequest, NextApiResponse } from 'next';
import { spawn } from 'child_process';
import path from 'path';

const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:5000';
const USE_EXTERNAL_API = process.env.USE_EXTERNAL_API === 'true';

// Helper function to safely get error message
const getErrorMessage = (error: unknown): string => {
	if (error instanceof Error) {
		return error.message;
	}
	return String(error);
};

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
			const response = await fetch(`${PYTHON_API_URL}/calculate_support_resistance`, {
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
				path.join(process.cwd(), 'strategies', 'support-resistance-blackflag-p1', 'support-resistance-blackflag-p1.py'),
				symbol as string,
				timeframe as string
			]);

			let result = '';
			let errorOutput = '';

			pythonProcess.stdout.on('data', (data) => {
				result += data.toString();
			});

			pythonProcess.stderr.on('data', (data) => {
				errorOutput += data.toString();
				console.error(`Python Error: ${data}`);
			});

			return new Promise((resolve, reject) => {
				pythonProcess.on('close', (code) => {
					if (code !== 0) {
						reject(res.status(500).json({ 
							message: 'Error executing Python script',
							error: errorOutput || result,
							details: {
								code,
								symbol,
								timeframe
							}
						}));
						return;
					}
					try {
						const jsonResult = JSON.parse(result);
						resolve(res.status(200).json(jsonResult));
					} catch (error) {
						reject(res.status(500).json({ 
							message: 'Error parsing Python result',
							error: getErrorMessage(error),
							rawResult: result
						}));
					}
				});

				pythonProcess.on('error', (error) => {
					console.error('Python Process Error:', error);
					reject(res.status(500).json({
						message: 'Failed to spawn Python process',
						error: getErrorMessage(error),
						details: {
							symbol,
							timeframe
						}
					}));
				});
			});
		}
	} catch (error) {
		console.error('API Error:', error);
		return res.status(500).json({ 
			message: 'Internal server error',
			error: getErrorMessage(error)
		});
	}
}