import React from 'react';

interface RiskHeatmapProps {
  riskData: Record<string, { count: number; avg_risk: number }>;
  'data-testid'?: string;
}

export const RiskHeatmap: React.FC<RiskHeatmapProps> = ({ riskData, 'data-testid': testId }) => {
  const healthStatuses = ['green', 'yellow', 'red'];
  const statusLabels = {
    green: 'On Track',
    yellow: 'At Risk',
    red: 'Critical'
  };

  const getColorIntensity = (status: string, count: number, maxCount: number) => {
    if (count === 0) return 'bg-gray-100';
    
    const intensity = Math.min(count / maxCount, 1);
    
    if (status === 'green') {
      return intensity > 0.7 ? 'bg-green-600' : intensity > 0.4 ? 'bg-green-400' : 'bg-green-200';
    } else if (status === 'yellow') {
      return intensity > 0.7 ? 'bg-yellow-600' : intensity > 0.4 ? 'bg-yellow-400' : 'bg-yellow-200';
    } else {
      return intensity > 0.7 ? 'bg-red-600' : intensity > 0.4 ? 'bg-red-400' : 'bg-red-200';
    }
  };

  const maxCount = Math.max(...Object.values(riskData).map(d => d.count), 1);

  return (
    <div className="space-y-4" data-testid={testId}>
      {/* Risk Matrix */}
      <div className="grid grid-cols-3 gap-4">
        {healthStatuses.map(status => {
          const data = riskData[status] || { count: 0, avg_risk: 0 };
          
          return (
            <div
              key={status}
              className={`p-4 rounded-lg border-2 transition-all hover:scale-105 ${getColorIntensity(status, data.count, maxCount)} ${
                data.count > 0 ? 'text-white' : 'text-gray-600'
              }`}
              data-testid={`risk-cell-${status}`}
            >
              <div className="text-center">
                <div className="text-2xl font-bold">{data.count}</div>
                <div className="text-sm font-medium">{statusLabels[status as keyof typeof statusLabels]}</div>
                <div className="text-xs mt-1">
                  Avg Risk: {(data.avg_risk * 100).toFixed(0)}%
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Legend */}
      <div className="flex items-center justify-center space-x-4 text-sm text-gray-600">
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-gray-100 rounded"></div>
          <span>No Projects</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-green-200 rounded"></div>
          <span>Low Count</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-green-400 rounded"></div>
          <span>Medium Count</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-green-600 rounded"></div>
          <span>High Count</span>
        </div>
      </div>
    </div>
  );
};