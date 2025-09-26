import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  PlusIcon,
  FunnelIcon,
  MagnifyingGlassIcon
} from '@heroicons/react/24/outline';
import { portfolioService } from '../../services/portfolioService';
import { Portfolio } from '../../types/portfolio';

export const PortfolioList: React.FC = () => {
  const [portfolios, setPortfolios] = useState<Portfolio[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    status: '',
    portfolio_type: '',
    search: ''
  });

  const fetchPortfolios = async () => {
    try {
      setLoading(true);
      const params = {
        ...filters,
        ...(filters.search && { search: filters.search })
      };
      const data = await portfolioService.getPortfolios(params);
      setPortfolios(data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load portfolios');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPortfolios();
  }, [filters]);

  const getStatusBadgeColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'on_hold': return 'bg-yellow-100 text-yellow-800';
      case 'completed': return 'bg-blue-100 text-blue-800';
      case 'cancelled': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getHealthBadgeColor = (health: string) => {
    switch (health) {
      case 'green': return 'bg-green-100 text-green-800';
      case 'yellow': return 'bg-yellow-100 text-yellow-800';
      case 'red': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="p-6" data-testid="portfolio-list">
      {/* Header */}
      <div className="sm:flex sm:items-center sm:justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Portfolios</h1>
          <p className="mt-2 text-sm text-gray-700">
            Manage your strategic portfolios and project collections
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <Link
            to="/portfolios/new"
            className="btn btn-primary flex items-center space-x-2"
            data-testid="create-portfolio-btn"
          >
            <PlusIcon className="h-5 w-5" />
            <span>New Portfolio</span>
          </Link>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Search */}
          <div className="relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search portfolios..."
              className="input pl-10"
              value={filters.search}
              onChange={(e) => setFilters({ ...filters, search: e.target.value })}
              data-testid="portfolio-search"
            />
          </div>

          {/* Status Filter */}
          <select
            className="input"
            value={filters.status}
            onChange={(e) => setFilters({ ...filters, status: e.target.value })}
            data-testid="status-filter"
          >
            <option value="">All Statuses</option>
            <option value="draft">Draft</option>
            <option value="active">Active</option>
            <option value="on_hold">On Hold</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </select>

          {/* Type Filter */}
          <select
            className="input"
            value={filters.portfolio_type}
            onChange={(e) => setFilters({ ...filters, portfolio_type: e.target.value })}
            data-testid="type-filter"
          >
            <option value="">All Types</option>
            <option value="strategic">Strategic</option>
            <option value="operational">Operational</option>
            <option value="innovation">Innovation</option>
            <option value="maintenance">Maintenance</option>
          </select>

          {/* Filter Button */}
          <button
            onClick={fetchPortfolios}
            className="btn btn-secondary flex items-center justify-center space-x-2"
          >
            <FunnelIcon className="h-4 w-4" />
            <span>Apply Filters</span>
          </button>
        </div>
      </div>

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
          <div className="text-red-800">{error}</div>
        </div>
      )}

      {/* Portfolio Grid */}
      {portfolios.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-500">
            {filters.search || filters.status || filters.portfolio_type
              ? 'No portfolios match your filters'
              : 'No portfolios created yet'}
          </div>
          {!filters.search && !filters.status && !filters.portfolio_type && (
            <Link
              to="/portfolios/new"
              className="btn btn-primary mt-4"
            >
              Create Your First Portfolio
            </Link>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {portfolios.map((portfolio) => (
            <Link
              key={portfolio.id}
              to={`/portfolios/${portfolio.id}`}
              className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow border border-gray-200"
              data-testid={`portfolio-card-${portfolio.id}`}
            >
              {/* Header */}
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-1">
                    {portfolio.name}
                  </h3>
                  <p className="text-sm text-gray-600 mb-2">
                    {portfolio.code}
                  </p>
                </div>
                <div className="flex space-x-2">
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusBadgeColor(portfolio.status)}`}>
                    {portfolio.status.replace('_', ' ').toUpperCase()}
                  </span>
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getHealthBadgeColor(portfolio.health_status)}`}>
                    {portfolio.health_status.toUpperCase()}
                  </span>
                </div>
              </div>

              {/* Description */}
              {portfolio.description && (
                <p className="text-sm text-gray-600 mb-4 line-clamp-2">
                  {portfolio.description}
                </p>
              )}

              {/* Metrics */}
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <div className="text-2xl font-bold text-gray-900">
                    {portfolio.project_count}
                  </div>
                  <div className="text-xs text-gray-500">Projects</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-gray-900">
                    {formatCurrency(portfolio.financial_metrics.total_budget)}
                  </div>
                  <div className="text-xs text-gray-500">Budget</div>
                </div>
              </div>

              {/* Budget Progress */}
              <div className="mb-4">
                <div className="flex justify-between text-xs text-gray-600 mb-1">
                  <span>Budget Utilization</span>
                  <span>{portfolio.budget_utilization_percentage.toFixed(1)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full"
                    style={{ width: `${Math.min(portfolio.budget_utilization_percentage, 100)}%` }}
                  ></div>
                </div>
              </div>

              {/* Footer */}
              <div className="flex justify-between items-center text-xs text-gray-500">
                <span>Updated {new Date(portfolio.updated_at).toLocaleDateString()}</span>
                <span className="capitalize">{portfolio.portfolio_type}</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};