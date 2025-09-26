import React from 'react';

interface ProjectStatusChartProps {
  data: Record<string, number>;
  'data-testid'?: string;
}

const statusColors = {
  draft: '#6B7280',
  active: '#10B981',
  on_hold: '#F59E0B',
  completed: '#3B82F6',
  cancelled: '#EF4444'
};

const statusLabels = {
  draft: 'Draft',
  active: 'Active',
  on_hold: 'On Hold',
  completed: 'Completed',
  cancelled: 'Cancelled'
};

export const ProjectStatusChart: React.FC<ProjectStatusChartProps> = ({ data, 'data-testid': testId }) => {
  const total = Object.values(data).reduce((sum, count) => sum + count, 0);
  
  if (total === 0) {
    return (
      <div className="text-center text-gray-500 py-8" data-testid={testId}>
        No projects to display
      </div>
    );
  }

  return (
    <div className="space-y-4" data-testid={testId}>
      {/* Donut Chart Simulation with Bars */}
      <div className="space-y-3">
        {Object.entries(data).map(([status, count]) => {
          const percentage = (count / total) * 100;
          
          return (
            <div key={status} className="flex items-center space-x-3">
              <div className="flex-1">
                <div className="flex justify-between items-center mb-1">
                  <div className="flex items-center space-x-2">
                    <div
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: statusColors[status as keyof typeof statusColors] }}
                    ></div>
                    <span className="text-sm font-medium text-gray-700">
                      {statusLabels[status as keyof typeof statusLabels]}
                    </span>
                  </div>
                  <span className="text-sm font-bold text-gray-900">
                    {count} ({percentage.toFixed(0)}%)
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="h-2 rounded-full transition-all duration-300"
                    style={{
                      width: `${percentage}%`,
                      backgroundColor: statusColors[status as keyof typeof statusColors]
                    }}
                    data-testid={`status-bar-${status}`}
                  ></div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Summary */}
      <div className="pt-4 border-t">
        <div className="flex justify-between items-center">
          <span className="text-sm font-medium text-gray-600">Total Projects:</span>
          <span className="text-lg font-bold text-gray-900" data-testid="total-projects">{total}</span>
        </div>
      </div>
    </div>
  );
};