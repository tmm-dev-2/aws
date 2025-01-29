export async function fetchCandleData(symbol: string, period: string) {
  try {
    const response = await fetch(`/api/candles?symbol=${symbol}&timeframe=${period}`);
    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching candle data:', error);
    return [];
  }
} 