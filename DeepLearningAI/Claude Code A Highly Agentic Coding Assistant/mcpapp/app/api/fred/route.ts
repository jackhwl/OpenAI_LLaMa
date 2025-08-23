import { NextRequest, NextResponse } from 'next/server';

interface FredDataPoint {
  date: string;
  value: string;
}

interface FredApiResponse {
  observations: FredDataPoint[];
}

const FRED_API_BASE = 'https://api.stlouisfed.org/fred';
const API_KEY = process.env.NEXT_PUBLIC_FRED_API_KEY;

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const seriesId = searchParams.get('series');
  const limit = searchParams.get('limit') || '50';

  if (!seriesId) {
    return NextResponse.json({ error: 'Series ID is required' }, { status: 400 });
  }

  if (!API_KEY) {
    return NextResponse.json({ error: 'FRED API key not configured' }, { status: 500 });
  }

  try {
    const response = await fetch(
      `${FRED_API_BASE}/series/observations?series_id=${seriesId}&api_key=${API_KEY}&file_type=json&observation_start=2023-07-01&limit=${limit}&sort_order=desc`
    );
    
    if (!response.ok) {
      throw new Error(`FRED API error: ${response.status}`);
    }
    
    const data: FredApiResponse = await response.json();
    
    const formattedData = data.observations
      .filter(obs => obs.value !== '.')
      .map(obs => ({
        date: new Date(obs.date).toLocaleDateString('en-US', { 
          year: 'numeric', 
          month: 'short' 
        }),
        value: parseFloat(obs.value)
      }))
      .reverse();

    return NextResponse.json(formattedData);
  } catch (error) {
    console.error('Error fetching FRED data:', error);
    return NextResponse.json({ error: 'Failed to fetch FRED data' }, { status: 500 });
  }
}