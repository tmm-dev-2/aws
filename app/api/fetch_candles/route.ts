import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const symbol = searchParams.get('symbol');
  const timeframe = searchParams.get('timeframe') || '1d';

  if (!symbol) {
    return NextResponse.json(
      { error: 'Symbol parameter is required' },
      { status: 400 }
    );
  }

  try {
    const response = await fetch(`http://localhost:5000/historical?symbol=${encodeURIComponent(symbol)}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    // Ensure we have a properly formatted response
    return NextResponse.json({
      candles: data.historical || [],
      bands: data.bands || {},
      backgrounds: data.backgrounds || [],
      signals: data.signals || []
    });

  } catch (error) {
    console.error('Error fetching data:', error);
    return NextResponse.json(
      { error: 'Failed to fetch data', candles: [] },
      { status: 500 }
    );
  }
} 