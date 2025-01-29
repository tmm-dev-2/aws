import type { NextApiRequest, NextApiResponse } from 'next';
import { exec } from 'child_process';

type Data = {
  results?: any;
  error?: string;
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  if (req.method !== 'POST') {
    return res.status(405).end();
  }

  const { formula, country, segment, timeframe } = req.body;

  if (!formula || !country || !segment || !timeframe) {
    return res.status(400).json({ error: 'Missing parameters' });
  }

  const command = `python pages/screenera_and_allert/generate_data.py "${formula}" ${country} ${segment} ${timeframe}`;

  try {
    const stdout = await new Promise<string>((resolve, reject) => {
      exec(command, (error: Error | null, stdout: string, stderr: string) => {
        if (error) {
          console.error(`exec error: ${error}`);
          reject(error);
          return;
        }
        if (stderr) {
          console.error(`stderr: ${stderr}`);
        }
        resolve(stdout);
      });
    });

    const response = await fetch('http://localhost:3000/market_data.json');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const results = await response.json();

    res.status(200).json({ results });
  } catch (error: any) {
    res.status(500).json({ error: error.message });
  }
}
