import React, { useState } from 'react';
import { CurrencyDollarIcon, ArrowTrendingUpIcon, ArrowTrendingDownIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';
import { ProjectDetail } from '../../types/project';

interface ProjectBudgetProps {
  projectDetail: ProjectDetail;
  onUpdate: () => void;
}

export const ProjectBudget: React.FC<ProjectBudgetProps> = ({
  projectDetail,
  onUpdate
}) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'breakdown' | 'forecast'>('overview');
  
  const { project } = projectDetail;
  const financials = project.financials;

  // Calculate budget metrics
  const budgetUtilization = (financials.spent_amount / financials.total_budget) * 100;
  const remainingBudget = financials.total_budget - financials.spent_amount;
  const isOverBudget = financials.spent_amount > financials.total_budget;
  const variancePercentage = ((financials.spent_amount - financials.total_budget) / financials.total_budget) * 100;

  // Mock cost breakdown data
  const costBreakdown = [
    {
      category: 'Labor',
      budgeted: financials.labor_cost,
      actual: financials.labor_cost * 0.85,
      percentage: 60
    },
    {
      category: 'Materials',
      budgeted: financials.material_cost,
      actual: financials.material_cost * 1.1,
      percentage: 20
    },
    {
      category: 'Vendors',
      budgeted: financials.vendor_cost,
      actual: financials.vendor_cost * 0.95,
      percentage: 15
    },
    {
      category: 'Overhead',
      budgeted: financials.overhead_cost,
      actual: financials.overhead_cost * 1.05,
      percentage: 5
    }
  ];

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const getStatusColor = (variance: number) => {
    if (variance > 10) return 'text-red-600 bg-red-50';
    if (variance > 5) return 'text-yellow-600 bg-yellow-50';
    return 'text-green-600 bg-green-50';
  };

  return (
    <div className="space-y-6" data-testid="project-budget">
      {/* Budget Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-lg shadow border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Budget</p>
              <p className="text-2xl font-bold text-gray-900" data-testid="total-budget">
                {formatCurrency(financials.total_budget)}
              </p>
            </div>
            <CurrencyDollarIcon className="h-8 w-8 text-gray-400" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Spent</p>
              <p className="text-2xl font-bold text-gray-900" data-testid="spent-amount">
                {formatCurrency(financials.spent_amount)}
              </p>
              <p className="text-sm text-gray-500">
                {budgetUtilization.toFixed(1)}% of budget
              </p>
            </div>
            <div className={`flex items-center ${isOverBudget ? 'text-red-500' : 'text-green-500'}`}>
              {isOverBudget ? <ArrowTrendingUpIcon className="h-8 w-8" /> : <ArrowTrendingDownIcon className="h-8 w-8" />}
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Remaining</p>
              <p className={`text-2xl font-bold ${remainingBudget >= 0 ? 'text-gray-900' : 'text-red-600'}`} data-testid="remaining-budget">
                {formatCurrency(remainingBudget)}
              </p>
            </div>
            {remainingBudget < 0 && <ExclamationTriangleIcon className="h-8 w-8 text-red-500" />}
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Forecast</p>
              <p className="text-2xl font-bold text-gray-900" data-testid="forecast-cost">
                {formatCurrency(financials.forecasted_cost)}
              </p>
              <p className={`text-sm ${variancePercentage > 0 ? 'text-red-500' : 'text-green-500'}`}>
                {variancePercentage > 0 ? '+' : ''}{variancePercentage.toFixed(1)}% variance
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8 px-6">
            {[
              { id: 'overview', name: 'Budget Overview' },
              { id: 'breakdown', name: 'Cost Breakdown' },
              { id: 'forecast', name: 'Forecast & Trends' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
                data-testid={`budget-tab-${tab.id}`}
              >
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Budget Progress */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-gray-700">Budget Utilization</span>
                  <span className="text-sm text-gray-500">{budgetUtilization.toFixed(1)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      budgetUtilization > 100 ? 'bg-red-600' :
                      budgetUtilization > 80 ? 'bg-yellow-500' : 'bg-green-500'
                    }`}
                    style={{ width: `${Math.min(budgetUtilization, 100)}%` }}
                    data-testid="budget-progress-bar"
                  ></div>
                </div>
              </div>

              {/* Key Metrics */}
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">Committed</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {formatCurrency(financials.committed_amount)}
                  </p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">Cost to Complete</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {formatCurrency(financials.cost_to_complete)}
                  </p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'breakdown' && (
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-gray-900">Cost Breakdown by Category</h3>
              
              {costBreakdown.map((category, index) => {
                const variance = ((category.actual - category.budgeted) / category.budgeted) * 100;
                
                return (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex justify-between items-center mb-2">
                      <h4 className="font-medium text-gray-900">{category.category}</h4>
                      <span className={`px-2 py-1 rounded text-sm font-medium ${getStatusColor(Math.abs(variance))}`}>
                        {variance > 0 ? '+' : ''}{variance.toFixed(1)}%
                      </span>
                    </div>
                    
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <p className="text-gray-600">Budgeted</p>
                        <p className="font-semibold">{formatCurrency(category.budgeted)}</p>
                      </div>
                      <div>
                        <p className="text-gray-600">Actual</p>
                        <p className="font-semibold">{formatCurrency(category.actual)}</p>
                      </div>
                      <div>
                        <p className="text-gray-600">Variance</p>
                        <p className={`font-semibold ${variance > 0 ? 'text-red-600' : 'text-green-600'}`}>
                          {formatCurrency(category.actual - category.budgeted)}
                        </p>
                      </div>
                    </div>
                    
                    {/* Progress bar for this category */}
                    <div className="mt-2">
                      <div className="w-full bg-gray-200 rounded-full h-1">
                        <div
                          className="h-1 rounded-full bg-primary-600"
                          style={{ width: `${(category.actual / category.budgeted) * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {activeTab === 'forecast' && (
            <div className="space-y-6">
              <h3 className="text-lg font-medium text-gray-900">Budget Forecast</h3>
              
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <TrendingUpIcon className="h-5 w-5 text-blue-400" />
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-blue-800">Forecast Analysis</h3>
                    <div className="mt-2 text-sm text-blue-700">
                      <p>Based on current spending trends, the project is expected to complete within budget with a forecasted total cost of {formatCurrency(financials.forecasted_cost)}.</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Forecast metrics */}
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 border rounded-lg">
                  <p className="text-sm text-gray-600">Projected Completion Cost</p>
                  <p className="text-xl font-bold text-gray-900">{formatCurrency(financials.forecasted_cost)}</p>
                  <p className="text-sm text-gray-500 mt-1">Based on current burn rate</p>
                </div>
                <div className="p-4 border rounded-lg">
                  <p className="text-sm text-gray-600">Budget Variance</p>
                  <p className={`text-xl font-bold ${financials.budget_variance >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {formatCurrency(Math.abs(financials.budget_variance))}
                  </p>
                  <p className="text-sm text-gray-500 mt-1">
                    {financials.budget_variance >= 0 ? 'Under budget' : 'Over budget'}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};