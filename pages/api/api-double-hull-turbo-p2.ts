import type { NextApiRequest, NextApiResponse } from 'next';
import { spawn } from 'child_process';
import path from 'path';

interface StrategyResult {
    hma1: number[];
    hma2: number[];
    crossover: number[];
    crossunder: number[];
    index: number[];
    valley_formation: number[];
    candle_direction: number[];
    candle_length: number[];
    box_data: Array<{
        time_index: number;
        high: number;
        low: number;
        color: string;
        transparency: number;
        extend: string;
    }>;
    timestamps: number[];
    visualization: {
        colors: {
            hma1_up: string;
            hma1_down: string;
            hma2_up: string;
            hma2_down: string;
        };
        transparency: number;
        box_color: string;
    };
}

const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:5000';
const USE_EXTERNAL_API = process.env.USE_EXTERNAL_API === 'true';

export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse<StrategyResult | { message: string; error?: string; exitCode?: number }>
) {
    if (req.method !== 'GET') {
        return res.status(405).json({ message: 'Method not allowed' });
    }

    const { symbol, timeframe, strategy } = req.query;

    if (!symbol || !timeframe) {
        return res.status(400).json({ message: 'Missing required parameters: symbol and timeframe' });
    }

    try {
        // External API route with enhanced error handling
        if (USE_EXTERNAL_API) {
            const response = await fetch(`${PYTHON_API_URL}/calculate_double_hull_turbo`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    symbol, 
                    timeframe, 
                    strategy,
                    version: 'p2' // Specify version for API differentiation
                }),
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Failed to fetch from Python API: ${response.statusText}. Details: ${errorText}`);
            }

            const data = await response.json();
            return res.status(200).json(data);
        } 
        
        // Local Python script execution with enhanced error handling
        const pythonProcess = spawn('python', [
            path.join(process.cwd(), 'strategies', 'double-hull-turbo', 'double-hull-turbo-p2.py'),
            symbol as string,
            timeframe as string,
            ...(strategy ? [strategy as string] : [])
        ]);

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