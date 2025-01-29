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

    const { symbol, timeframe, strategy } = req.query;

    if (!symbol || !timeframe) {
        return res.status(400).json({ message: 'Missing required parameters: symbol and timeframe' });
    }

    try {
        // External API route
        if (USE_EXTERNAL_API) {
            const response = await fetch(`${PYTHON_API_URL}/double-hull-turbo-p1?symbol=${symbol}&timeframe=${timeframe}`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error(`Failed to fetch from Python API: ${response.statusText}`);
            }

            const data = await response.json();
            return res.status(200).json(data);
        } 
        
        // Local Python script execution
        const pythonProcess = spawn('python3', [
            path.join(process.cwd(), 'strategies', 'double-hull-turbo-p1', 'double-hull-turbo-p1.py'),
            symbol as string,
            timeframe as string,
            ...(strategy ? [strategy as string] : [])
        ]);

        let result = '';
        let errorOutput = '';

        // Capture standard output
        pythonProcess.stdout.on('data', (data) => {
            result += data.toString();
        });

        // Capture error output
        pythonProcess.stderr.on('data', (data) => {
            errorOutput += data.toString();
            console.error(`Python stderr: ${data}`);
        });

        return new Promise((resolve, reject) => {
            pythonProcess.on('close', (code) => {
                // Handle non-zero exit codes
                if (code !== 0) {
                    console.error(`Python process exited with code ${code}`);
                    return reject(res.status(500).json({ 
                        message: 'Error executing Python script',
                        error: errorOutput,
                        exitCode: code
                    }));
                }

                // Parse JSON result
                try {
                    const jsonResult = JSON.parse(result.trim());
                    resolve(res.status(200).json(jsonResult));
                } catch (parseError) {
                    console.error('JSON parsing error:', parseError);
                    reject(res.status(500).json({ 
                        message: 'Error parsing Python result',
                        error: parseError instanceof Error ? parseError.message : 'Unknown parsing error',
                        rawOutput: result
                    }));
                }
            });

            // Handle process spawning errors
            pythonProcess.on('error', (error) => {
                console.error('Python process spawn error:', error);
                reject(res.status(500).json({ 
                    message: 'Error spawning Python process',
                    error: error.message 
                }));
            });
        });
    } catch (error) {
        console.error('API Handler Error:', error);
        return res.status(500).json({ 
            message: 'Internal server error',
            error: error instanceof Error ? error.message : 'Unknown error'
        });
    }
}
