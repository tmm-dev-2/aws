import React from 'react';

interface StatisticsTableProps {
  data: { [key: string]: string | number | null };
}

const StatisticsTable: React.FC<StatisticsTableProps> = ({ data }) => {
  return (
    <div className="overflow-x-auto">
      <h3 className="text-lg font-semibold mb-4">Statistics</h3>
      <table className="min-w-full divide-y divide-gray-700">
        <thead>
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider bg-[#1a1a1a]">
              Metric
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider bg-[#1a1a1a]">
              Value
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-700">
          {Object.entries(data).map(([metric, value], index) => (
            <tr key={metric} className={index % 2 === 0 ? 'bg-[#1a1a1a]' : 'bg-[#242424]'}>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                {metric.replace(/([A-Z])/g, ' $1').trim()}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                {value !== null ? value.toString() : '-'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StatisticsTable;
