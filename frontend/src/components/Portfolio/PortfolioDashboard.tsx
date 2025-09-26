import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  ChartBarIcon,
  CurrencyDollarIcon,
  ExclamationTriangleIcon,
  FolderIcon,
  PlusIcon
} from '@heroicons/react/24/outline';
import { portfolioService } from '../../services/portfolioService';
import { Portfolio, PortfolioDashboard as PortfolioDashboardType } from '../../types/portfolio';
import { KPICard } from './KPICard';
import { RiskHeatmap } from './RiskHeatmap';
import { BudgetChart } from './BudgetChart';
import { ProjectStatusChart } from './ProjectStatusChart';
import { QuickActions } from './QuickActions';

interface PortfolioDashboardProps {
  portfolioId?: string;
}

export const PortfolioDashboard: React.FC<PortfolioDashboardProps> = ({ portfolioId: propPortfolioId }) => {
  const { portfolioId: paramPortfolioId } = useParams<{ portfolioId: string }>();
  const portfolioId = propPortfolioId || paramPortfolioId;

  const [dashboard, setDashboard] = useState<PortfolioDashboardType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchDashboard = async () => {
    if (!portfolioId) return;
    
    try {
      setRefreshing(true);
      const data = await portfolioService.getPortfolioDashboard(portfolioId);
      setDashboard(data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load portfolio dashboard');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, [portfolioId]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error || !dashboard) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <ExclamationTriangleIcon className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Error Loading Dashboard</h3>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={fetchDashboard}
            className="btn btn-primary"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const { portfolio, kpis } = dashboard;

  return (
    <div className="p-6 space-y-6" data-testid="portfolio-dashboard">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900" data-testid="portfolio-name">
            {portfolio.name}
          </h1>
          <p className="text-gray-600 mt-1">{portfolio.description}</p>
          <div className="flex items-center space-x-4 mt-2">
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
              portfolio.status === 'active' ? 'bg-green-100 text-green-800' :
              portfolio.status === 'on_hold' ? 'bg-yellow-100 text-yellow-800' :
              'bg-gray-100 text-gray-800'
            }`}>
              {portfolio.status.replace('_', ' ').toUpperCase()}
            </span>
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
              portfolio.health_status === 'green' ? 'bg-green-100 text-green-800' :
              portfolio.health_status === 'yellow' ? 'bg-yellow-100 text-yellow-800' :
              'bg-red-100 text-red-800'
            }`}>
              {portfolio.health_status.toUpperCase()}
            </span>
          </div>
        </div>
        
        <div className="flex space-x-3">
          <button
            onClick={fetchDashboard}
            disabled={refreshing}
            className="btn btn-secondary"
            data-testid="refresh-dashboard-btn"
          >
            {refreshing ? 'Refreshing...' : 'Refresh'}
          </button>
          <QuickActions portfolioId={portfolio.id} />
        </div>
      </div>

      {/* KPI Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPICard
          title="Total Projects"
          value={kpis.total_projects}
          icon={FolderIcon}
          color="blue"
          data-testid="total-projects-card"
        />
        <KPICard
          title="Budget Utilization"
          value={`${kpis.budget_utilization_percentage.toFixed(1)}%`}
          icon={CurrencyDollarIcon}
          color="green"
          subtitle={`$${(kpis.budget_summary.total_spent / 1000000).toFixed(1)}M of $${(kpis.budget_summary.total_budget / 1000000).toFixed(1)}M`}
          data-testid="budget-utilization-card"
        />
        <KPICard
          title="Active Projects"
          value={kpis.status_counts.active || 0}
          icon={ChartBarIcon}
          color="indigo"
          subtitle={`${portfolio.active_project_count} active`}
          data-testid="active-projects-card"
        />
        <KPICard
          title="Risk Score"
          value={portfolio.risk_metrics.risk_score.toFixed(2)}
          icon={ExclamationTriangleIcon}
          color={portfolio.risk_metrics.risk_score > 0.7 ? 'red' : portfolio.risk_metrics.risk_score > 0.4 ? 'yellow' : 'green'}
          subtitle={`${portfolio.risk_metrics.high_risks_count} high risks`}
          data-testid="risk-score-card"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Project Status Distribution */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Project Status Distribution</h3>
          <ProjectStatusChart
            data={kpis.status_counts}
            data-testid="project-status-chart"
          />
        </div>

        {/* Budget Overview */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Budget Overview</h3>
          <BudgetChart
            budgetData={kpis.budget_summary}
            data-testid="budget-chart"
          />
        </div>
      </div>

      {/* Risk Heatmap and Additional Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risk Heatmap */}
        <div className="lg:col-span-2 bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Risk Heatmap</h3>
          <RiskHeatmap
            riskData={kpis.risk_heatmap}
            data-testid="risk-heatmap"
          />
        </div>

        {/* Key Metrics */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Key Metrics</h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between">
                <span className="text-sm font-medium text-gray-500">Projects On Track</span>
                <span className="text-sm font-bold text-green-600">
                  {kpis.risk_heatmap.green?.count || 0}
                </span>
              </div>
            </div>
            <div>
              <div className="flex justify-between">
                <span className="text-sm font-medium text-gray-500">Projects At Risk</span>
                <span className="text-sm font-bold text-yellow-600">
                  {kpis.risk_heatmap.yellow?.count || 0}
                </span>
              </div>
            </div>
            <div>
              <div className="flex justify-between">
                <span className="text-sm font-medium text-gray-500">Critical Projects</span>
                <span className="text-sm font-bold text-red-600">
                  {kpis.risk_heatmap.red?.count || 0}
                </span>
              </div>
            </div>
            <div className="pt-2 border-t">
              <div className="flex justify-between">
                <span className="text-sm font-medium text-gray-500">Budget Remaining</span>
                <span className="text-sm font-bold text-blue-600">
                  ${((kpis.budget_summary.total_budget - kpis.budget_summary.total_spent) / 1000000).toFixed(1)}M
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity & Quick Links */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Activity</h3>
          <div className="space-y-3">
            <div className="text-sm text-gray-600">
              No recent activity data available.
            </div>
          </div>
        </div>

        {/* Quick Links */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-2 gap-3">
            <button className="btn btn-outline text-left p-3">
              <PlusIcon className="h-5 w-5 mb-2" />
              <div className="text-sm font-medium">Add Project</div>
            </button>
            <button className="btn btn-outline text-left p-3">
              <ChartBarIcon className="h-5 w-5 mb-2" />
              <div className="text-sm font-medium">View Reports</div>
            </button>
            <button className="btn btn-outline text-left p-3">
              <ExclamationTriangleIcon className="h-5 w-5 mb-2" />
              <div className="text-sm font-medium">Risk Review</div>
            </button>
            <button className="btn btn-outline text-left p-3">
              <CurrencyDollarIcon className="h-5 w-5 mb-2" />
              <div className="text-sm font-medium">Budget Review</div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PortfolioDashboard;