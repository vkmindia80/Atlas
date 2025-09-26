import React, { useEffect, useState } from 'react';
import { PlusIcon, FolderIcon } from '@heroicons/react/24/outline';
import { Portfolio, PortfolioType, Priority, Status, HealthStatus } from '../types/portfolio';
import { apiService } from '../services/api';

export const Portfolios: React.FC = () => {
  const [portfolios, setPortfolios] = useState<Portfolio[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPortfolios = async () => {
      try {
        const data = await apiService.get<Portfolio[]>('/api/v1/portfolios');
        setPortfolios(data);
      } catch (error: any) {
        setError('Failed to fetch portfolios');
        console.error('Error fetching portfolios:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPortfolios();
  }, []);

  const getStatusColor = (status: Status) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'draft': return 'bg-gray-100 text-gray-800';
      case 'on_hold': return 'bg-yellow-100 text-yellow-800';
      case 'completed': return 'bg-blue-100 text-blue-800';
      case 'cancelled': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getHealthColor = (health: HealthStatus) => {
    switch (health) {
      case HealthStatus.GREEN: return 'bg-green-500';
      case HealthStatus.YELLOW: return 'bg-yellow-500';
      case HealthStatus.RED: return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getPriorityColor = (priority: Priority) => {
    switch (priority) {
      case 'critical': return 'text-red-600';
      case 'high': return 'text-orange-600';
      case 'medium': return 'text-yellow-600';
      case 'low': return 'text-green-600';
      default: return 'text-gray-600';
    }
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
          <div className="space-y-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="bg-white shadow rounded-lg p-6">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="rounded-md bg-red-50 p-4">
          <div className="text-sm text-red-700">{error}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-semibold text-gray-900">Portfolios</h1>
          <p className="mt-2 text-sm text-gray-700">
            Manage your investment portfolios and strategic initiatives.
          </p>
        </div>
        <div className="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
          <button
            type="button"
            className="inline-flex items-center justify-center rounded-md border border-transparent bg-primary-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
          >
            <PlusIcon className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
            New Portfolio
          </button>
        </div>
      </div>

      {portfolios.length === 0 ? (
        <div className="text-center py-12">
          <FolderIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No portfolios</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by creating a new portfolio.</p>
          <div className="mt-6">
            <button
              type="button"
              className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <PlusIcon className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
              New Portfolio
            </button>
          </div>
        </div>
      ) : (
        <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {portfolios.map((portfolio) => (
            <div key={portfolio.id} className="bg-white shadow-sm rounded-lg overflow-hidden hover:shadow-md transition-shadow">
              <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center">
                    <div className={`w-3 h-3 rounded-full ${getHealthColor(portfolio.health_status)} mr-2`}></div>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(portfolio.status)}`}>
                      {portfolio.status.replace('_', ' ').toUpperCase()}
                    </span>
                  </div>
                  <span className={`text-sm font-medium ${getPriorityColor(portfolio.priority)}`}>
                    {portfolio.priority.toUpperCase()}
                  </span>
                </div>

                <h3 className="text-lg font-medium text-gray-900 mb-2">{portfolio.name}</h3>
                <p className="text-sm text-gray-600 mb-2">Code: {portfolio.code}</p>
                {portfolio.description && (
                  <p className="text-sm text-gray-500 mb-4 line-clamp-2">{portfolio.description}</p>
                )}

                <div className="flex justify-between items-center text-sm text-gray-500 mb-4">
                  <span>{portfolio.portfolio_type.replace('_', ' ').toUpperCase()}</span>
                  <span>{portfolio.project_count} projects</span>
                </div>

                <div className="border-t pt-4">
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-gray-500">Budget:</span>
                    <span className="font-medium">
                      ${portfolio.financial_metrics.total_budget.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between items-center text-sm mt-1">
                    <span className="text-gray-500">Spent:</span>
                    <span className="font-medium">
                      ${portfolio.financial_metrics.spent_amount.toLocaleString()}
                    </span>
                  </div>
                </div>

                <div className="mt-4 flex justify-between">
                  <button className="text-primary-600 hover:text-primary-900 text-sm font-medium">
                    View Details
                  </button>
                  <button className="text-gray-400 hover:text-gray-600 text-sm">
                    Edit
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};