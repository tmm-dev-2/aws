import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const symbol = searchParams.get('symbol');

  if (!symbol) {
    return NextResponse.json(
      { valid: false, error: 'Symbol parameter is required' },
      { status: 400 }
    );
  }

  try {
    // Check if data is available for this symbol
    const response = await fetch(
      `http://localhost:5000/validate_symbol?symbol=${encodeURIComponent(symbol)}`
    );
    const data = await response.json();

    return NextResponse.json({ valid: data.valid });
  } catch (error) {
    console.error('Error validating symbol:', error);
    return NextResponse.json(
      { valid: false, error: 'Failed to validate symbol' },
      { status: 500 }
    );
  }
} 