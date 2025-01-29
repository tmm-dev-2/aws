import React from 'react';

interface CashFlowProps {
  data: { [key: string]: { [key: string]: string | null } };
}

const CashFlow: React.FC<CashFlowProps> = ({ data }) => {
  // Get dates (columns) from the first metric
  const firstMetric = data ? Object.values(data)[0] : {};
  const dates = firstMetric ? Object.keys(firstMetric).sort().reverse() : [];

  // Format number to millions/billions
  const formatNumber = (value: string | null) => {
    if (!value) return '-';
    const num = parseFloat(value);
    if (isNaN(num)) return '-';

    if (Math.abs(num) >= 1e9) {
      return `${(num / 1e9).toFixed(2)}B`;
    } else if (Math.abs(num) >= 1e6) {
      return `${(num / 1e6).toFixed(2)}M`;
    } else {
      return num.toFixed(2);
    }
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-700">
        <thead>
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider bg-[#1a1a1a]">
              Metric
            </th>
            {dates.map((date) => (
              <th
                key={date}
                className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider bg-[#1a1a1a]"
              >
                {new Date(date).getFullYear()}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-700">
          {Object.entries(data).map(([metric, values], index) => (
            <tr key={metric} className={index % 2 === 0 ? 'bg-[#1a1a1a]' : 'bg-[#242424]'}>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                {metric.replace(/([A-Z])/g, ' $1').trim()}
              </td>
              {dates.map((date) => (
                <td key={date} className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                  {formatNumber(values ? values[date] : null)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CashFlow;