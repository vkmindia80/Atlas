import React from 'react';

interface BudgetChartProps {
  budgetData: {
    total_budget: number;
    total_spent: number;
    total_committed: number;
  };
  'data-testid'?: string;
}

export const BudgetChart: React.FC<BudgetChartProps> = ({ budgetData, 'data-testid': testId }) => {
  const { total_budget, total_spent, total_committed } = budgetData;
  
  const spentPercentage = total_budget > 0 ? (total_spent / total_budget) * 100 : 0;
  const committedPercentage = total_budget > 0 ? (total_committed / total_budget) * 100 : 0;
  const availablePercentage = 100 - spentPercentage - committedPercentage;

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  return (
    <div className="space-y-4" data-testid={testId}>
      {/* Budget Bar Chart */}
      <div className="relative">
        <div className="flex h-8 bg-gray-200 rounded-full overflow-hidden">
          <div
            className="bg-red-500 flex items-center justify-center text-xs font-medium text-white"
            style={{ width: `${spentPercentage}%` }}
            data-testid="spent-bar"
          >
            {spentPercentage > 10 && `${spentPercentage.toFixed(0)}%`}
          </div>
          <div
            className="bg-yellow-500 flex items-center justify-center text-xs font-medium text-white"
            style={{ width: `${committedPercentage}%` }}
            data-testid="committed-bar"
          >
            {committedPercentage > 10 && `${committedPercentage.toFixed(0)}%`}
          </div>
          <div
            className="bg-green-500 flex items-center justify-center text-xs font-medium text-white"
            style={{ width: `${availablePercentage}%` }}
            data-testid="available-bar"
          >
            {availablePercentage > 10 && `${availablePercentage.toFixed(0)}%`}
          </div>
        </div>
      </div>

      {/* Budget Legend */}
      <div className="grid grid-cols-3 gap-4 text-sm">
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-red-500 rounded-full"></div>
          <div>
            <div className="font-medium">Spent</div>
            <div className="text-gray-600">{formatCurrency(total_spent)}</div>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
          <div>
            <div className="font-medium">Committed</div>
            <div className="text-gray-600">{formatCurrency(total_committed)}</div>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-green-500 rounded-full"></div>
          <div>
            <div className="font-medium">Available</div>
            <div className="text-gray-600">{formatCurrency(total_budget - total_spent - total_committed)}</div>
          </div>
        </div>
      </div>

      {/* Budget Summary */}
      <div className="pt-4 border-t space-y-2">
        <div className="flex justify-between">
          <span className="font-medium">Total Budget:</span>
          <span className="font-bold">{formatCurrency(total_budget)}</span>
        </div>
        <div className="flex justify-between text-sm text-gray-600">
          <span>Utilization Rate:</span>
          <span>{((total_spent + total_committed) / total_budget * 100).toFixed(1)}%</span>
        </div>
      </div>
    </div>
  );
};