export async function fetchFredSeries(seriesId: string, limit = 50): Promise<any[]> {
  try {
    const response = await fetch(`/api/fred?series=${seriesId}&limit=${limit}`);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching FRED data:', error);
    return [];
  }
}

export const FRED_SERIES_IDS = {
  CPI: 'CPIAUCSL',                    // Consumer Price Index for All Urban Consumers
  UNEMPLOYMENT: 'UNRATE',             // Unemployment Rate
  BOND_10Y: 'GS10',                   // 10-Year Treasury Constant Maturity Rate
  BOND_3M: 'GS3M',                    // 3-Month Treasury Constant Maturity Rate
  GDP: 'GDP',                         // Gross Domestic Product
  EXCHANGE_RATE_EUR: 'DEXUSEU',       // US / Euro Foreign Exchange Rate
  HOUSING_STARTS: 'HOUST',            // Housing Starts
  CONSUMER_SPENDING: 'PCE'            // Personal Consumption Expenditures
};