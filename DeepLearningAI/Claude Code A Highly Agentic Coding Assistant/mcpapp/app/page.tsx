'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { useEffect, useState } from 'react';
import { fetchFredSeries, FRED_SERIES_IDS } from '../lib/fredApi';


export default function Home() {
  const [cpiData, setCpiData] = useState<any[]>([]);
  const [unemploymentData, setUnemploymentData] = useState<any[]>([]);
  const [bondYieldData, setBondYieldData] = useState<any[]>([]);
  const [shortRateData, setShortRateData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [cpi, unemployment, bondYield, shortRate] = await Promise.all([
          fetchFredSeries(FRED_SERIES_IDS.CPI, 60),
          fetchFredSeries(FRED_SERIES_IDS.UNEMPLOYMENT, 24),
          fetchFredSeries(FRED_SERIES_IDS.BOND_10Y, 60),
          fetchFredSeries(FRED_SERIES_IDS.BOND_3M, 60)
        ]);
        
        setCpiData(cpi);
        setUnemploymentData(unemployment.map(item => ({ ...item, rate: item.value })));
        setBondYieldData(bondYield.map(item => ({ ...item, yield: item.value })));
        setShortRateData(shortRate.map(item => ({ ...item, rate: item.value })));
      } catch (error) {
        console.error('Failed to fetch FRED data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex h-screen bg-gray-50 items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading FRED economic data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <aside className="w-64 bg-white border-r border-gray-200 p-4">
        <div className="mb-8">
          <h1 className="text-lg font-bold text-gray-900">FRED Indicators</h1>
          <p className="text-sm text-gray-600">Economic Data Dashboard</p>
        </div>
        
        <nav className="space-y-2">
          <div className="bg-blue-50 text-blue-700 px-3 py-2 rounded-md flex items-center">
            <span className="mr-2">📊</span>
            Key Indicators
          </div>
          <div className="text-gray-700 px-3 py-2 hover:bg-gray-50 rounded-md flex items-center cursor-pointer">
            <span className="mr-2">📈</span>
            Inflation
          </div>
          <div className="text-gray-700 px-3 py-2 hover:bg-gray-50 rounded-md flex items-center cursor-pointer">
            <span className="mr-2">💼</span>
            Employment
          </div>
          <div className="text-gray-700 px-3 py-2 hover:bg-gray-50 rounded-md flex items-center cursor-pointer">
            <span className="mr-2">📊</span>
            Interest Rates
          </div>
          <div className="text-gray-700 px-3 py-2 hover:bg-gray-50 rounded-md flex items-center cursor-pointer">
            <span className="mr-2">📈</span>
            Economic Growth
          </div>
          <div className="text-gray-700 px-3 py-2 hover:bg-gray-50 rounded-md flex items-center cursor-pointer">
            <span className="mr-2">🌐</span>
            Exchange Rates
          </div>
          <div className="text-gray-700 px-3 py-2 hover:bg-gray-50 rounded-md flex items-center cursor-pointer">
            <span className="mr-2">🏠</span>
            Housing
          </div>
          <div className="text-gray-700 px-3 py-2 hover:bg-gray-50 rounded-md flex items-center cursor-pointer">
            <span className="mr-2">🛒</span>
            Consumer Spending
          </div>
        </nav>
        
        <div className="mt-8 text-xs text-gray-500">
          <p>Data provided by Federal Reserve Economic Data (FRED)</p>
        </div>
      </aside>

      <main className="flex-1 p-6">
        <header className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Economic Indicators Dashboard
          </h1>
          <p className="text-gray-600">
            Real-time economic data from the Federal Reserve Economic Data (FRED) system
          </p>
        </header>

        <div className="grid grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg border border-gray-200">
            <h3 className="text-lg font-semibold mb-2 text-gray-900">
              Consumer Price Index (CPI)
            </h3>
            <p className="text-sm text-gray-600 mb-4">FRED - All Urban Consumers, All Items (CPIAUCSL)</p>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={cpiData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="date" stroke="#666" fontSize={11} />
                  <YAxis stroke="#666" fontSize={11} domain={['dataMin - 10', 'dataMax + 10']} />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#fff', 
                      border: '1px solid #ccc',
                      borderRadius: '4px'
                    }} 
                  />
                  <Line 
                    type="monotone" 
                    dataKey="value" 
                    stroke="#3b82f6" 
                    strokeWidth={2}
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <p className="text-xs text-gray-500 mt-2">Last Updated: {new Date().toLocaleDateString()} • View Details &gt;</p>
          </div>

          <div className="bg-white p-6 rounded-lg border border-gray-200">
            <h3 className="text-lg font-semibold mb-2 text-gray-900">
              Unemployment Rate
            </h3>
            <p className="text-sm text-gray-600 mb-4">FRED - Civilian Unemployment Rate (UNRATE)</p>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={unemploymentData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="date" stroke="#666" fontSize={11} />
                  <YAxis stroke="#666" fontSize={11} domain={[0, 'dataMax + 1']} />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#fff', 
                      border: '1px solid #ccc',
                      borderRadius: '4px'
                    }} 
                  />
                  <Area 
                    type="monotone" 
                    dataKey="rate" 
                    stroke="#10b981" 
                    fill="#10b981"
                    fillOpacity={0.3}
                    strokeWidth={2}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
            <p className="text-xs text-gray-500 mt-2">Last Updated: {new Date().toLocaleDateString()} • View Details &gt;</p>
          </div>

          <div className="bg-white p-6 rounded-lg border border-gray-200">
            <h3 className="text-lg font-semibold mb-2 text-gray-900">
              10-Year Treasury Yield
            </h3>
            <p className="text-sm text-gray-600 mb-4">FRED - Market Yield on U.S. Treasury Securities (GS10)</p>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={bondYieldData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="date" stroke="#666" fontSize={11} />
                  <YAxis stroke="#666" fontSize={11} domain={['dataMin - 0.5', 'dataMax + 0.5']} />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#fff', 
                      border: '1px solid #ccc',
                      borderRadius: '4px'
                    }} 
                  />
                  <Line 
                    type="monotone" 
                    dataKey="yield" 
                    stroke="#8b5cf6" 
                    strokeWidth={2}
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <p className="text-xs text-gray-500 mt-2">Last Updated: {new Date().toLocaleDateString()} • View Details &gt;</p>
          </div>

          <div className="bg-white p-6 rounded-lg border border-gray-200">
            <h3 className="text-lg font-semibold mb-2 text-gray-900">
              3-Month Treasury Yield
            </h3>
            <p className="text-sm text-gray-600 mb-4">FRED - Market Yield on U.S. Treasury Securities (GS3M)</p>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={shortRateData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="date" stroke="#666" fontSize={11} />
                  <YAxis stroke="#666" fontSize={11} domain={['dataMin - 0.5', 'dataMax + 0.5']} />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#fff', 
                      border: '1px solid #ccc',
                      borderRadius: '4px'
                    }} 
                  />
                  <Line 
                    type="monotone" 
                    dataKey="rate" 
                    stroke="#f59e0b" 
                    strokeWidth={2}
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <p className="text-xs text-gray-500 mt-2">Last Updated: {new Date().toLocaleDateString()} • View Details &gt;</p>
          </div>
        </div>
      </main>
    </div>
  );
}
