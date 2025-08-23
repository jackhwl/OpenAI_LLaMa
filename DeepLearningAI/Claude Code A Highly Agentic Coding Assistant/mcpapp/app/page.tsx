'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const sampleCPIData = [
  { year: '2019', value: 255.7 },
  { year: '2020', value: 258.8 },
  { year: '2021', value: 270.9 },
  { year: '2022', value: 292.7 },
  { year: '2023', value: 307.0 },
  { year: '2024', value: 310.3 }
];

const sampleUnemploymentData = [
  { date: 'Jan 2023', rate: 3.4 },
  { date: 'Apr 2023', rate: 3.4 },
  { date: 'Jul 2023', rate: 3.5 },
  { date: 'Oct 2023', rate: 3.9 },
  { date: 'Jan 2024', rate: 3.7 },
  { date: 'Apr 2024', rate: 3.9 }
];

const sampleBondYieldData = [
  { date: 'Jan 2020', yield: 1.5 },
  { date: 'Jan 2021', yield: 1.0 },
  { date: 'Jan 2022', yield: 1.8 },
  { date: 'Jan 2023', yield: 3.5 },
  { date: 'Jan 2024', yield: 4.2 }
];

const sampleShortRateData = [
  { date: 'Jan 2020', rate: 1.6 },
  { date: 'Jan 2021', rate: 0.1 },
  { date: 'Jan 2022', rate: 0.2 },
  { date: 'Jan 2023', rate: 4.3 },
  { date: 'Jan 2024', rate: 5.4 }
];

export default function Home() {
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
            <h3 className="text-lg font-semibold mb-4 text-gray-900">
              CPI - last five years
            </h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={sampleCPIData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="year" stroke="#666" fontSize={12} />
                  <YAxis stroke="#666" fontSize={12} />
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
                    stroke="#2563eb" 
                    strokeWidth={2}
                    dot={{ fill: '#2563eb', strokeWidth: 2, r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <p className="text-xs text-gray-500 mt-2">FRED</p>
          </div>

          <div className="bg-white p-6 rounded-lg border border-gray-200">
            <h3 className="text-lg font-semibold mb-4 text-gray-900">
              Infra-Annual Labor Statistics: Unemployment Rate Total
            </h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={sampleUnemploymentData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="date" stroke="#666" fontSize={12} />
                  <YAxis stroke="#666" fontSize={12} />
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
                    stroke="#2563eb" 
                    strokeWidth={2}
                    dot={{ fill: '#2563eb', strokeWidth: 2, r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <p className="text-xs text-gray-500 mt-2">FRED</p>
          </div>

          <div className="bg-white p-6 rounded-lg border border-gray-200">
            <h3 className="text-lg font-semibold mb-4 text-gray-900">
              Interest Rates: Long-Term Government Bond Yields: 10-Year
            </h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={sampleBondYieldData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="date" stroke="#666" fontSize={12} />
                  <YAxis stroke="#666" fontSize={12} />
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
                    stroke="#2563eb" 
                    strokeWidth={2}
                    dot={{ fill: '#2563eb', strokeWidth: 2, r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <p className="text-xs text-gray-500 mt-2">FRED</p>
          </div>

          <div className="bg-white p-6 rounded-lg border border-gray-200">
            <h3 className="text-lg font-semibold mb-4 text-gray-900">
              Interest Rates: 3-Month or 90-Day Rates and Yields
            </h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={sampleShortRateData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="date" stroke="#666" fontSize={12} />
                  <YAxis stroke="#666" fontSize={12} />
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
                    stroke="#2563eb" 
                    strokeWidth={2}
                    dot={{ fill: '#2563eb', strokeWidth: 2, r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <p className="text-xs text-gray-500 mt-2">FRED</p>
          </div>
        </div>
      </main>
    </div>
  );
}
