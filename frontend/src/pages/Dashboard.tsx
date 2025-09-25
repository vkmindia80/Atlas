import React, { useEffect, useState } from 'react';
import {
  FolderIcon,
  BriefcaseIcon,
  UsersIcon,
  CurrencyDollarIcon,
} from '@heroicons/react/24/outline';
import { useAuth } from '../store/AuthContext';
import { apiService } from '../services/api';
import { UserRole } from '../types/auth';

interface DashboardStats {
  overview: {
    total_users: number;
    total_portfolios: number;
    total_projects: number;
  };
  project_status_distribution: Record<string, number>;
  users_by_role: Record<string, number>;
  recent_activity: {
    new_users_30_days: number;
    new_projects_30_days: number;
  };
}

export const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        if (user?.role === UserRole.ADMIN || user?.role === UserRole.PMO_ADMIN) {
          const dashboardData = await apiService.get<DashboardStats>('/api/v1/admin/dashboard');
          setStats(dashboardData);
        }
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [user]);

  const statCards = [
    {
      name: 'Total Portfolios',
      value: stats?.overview.total_portfolios || 0,
      icon: FolderIcon,
      color: 'bg-blue-500',
    },
    {
      name: 'Total Projects',
      value: stats?.overview.total_projects || 0,
      icon: BriefcaseIcon,
      color: 'bg-green-500',
    },
    {
      name: 'Total Users',
      value: stats?.overview.total_users || 0,
      icon: UsersIcon,
      color: 'bg-purple-500',
    },
    {
      name: 'New Projects (30d)',
      value: stats?.recent_activity.new_projects_30_days || 0,
      icon: CurrencyDollarIcon,
      color: 'bg-orange-500',
    },
  ];

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="bg-white overflow-hidden shadow rounded-lg">
                <div className="p-5">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 bg-gray-200 rounded"></div>
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                      <div className="h-6 bg-gray-200 rounded w-1/2"></div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">
          Welcome back, {user?.full_name?.split(' ')[0]}!
        </h1>
        <p className="mt-1 text-sm text-gray-600">
          Here's what's happening with your projects and portfolios today.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        {statCards.map((item) => (
          <div key={item.name} className="bg-white overflow-hidden shadow-sm rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className={`w-10 h-10 ${item.color} rounded-lg flex items-center justify-center`}>
                    <item.icon className="w-6 h-6 text-white" />
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      {item.name}
                    </dt>
                    <dd className="text-2xl font-semibold text-gray-900">
                      {item.value.toLocaleString()}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Project Status Distribution */}
      {stats?.project_status_distribution && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white shadow-sm rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Project Status Distribution</h3>
            <div className="space-y-3">
              {Object.entries(stats.project_status_distribution).map(([status, count]) => (
                <div key={status} className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-600 capitalize">
                    {status.replace('_', ' ')}
                  </span>
                  <span className="text-sm text-gray-900">{count}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white shadow-sm rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Users by Role</h3>
            <div className="space-y-3">
              {Object.entries(stats.users_by_role || {}).map(([role, count]) => (
                <div key={role} className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-600 capitalize">
                    {role.replace('_', ' ')}
                  </span>
                  <span className="text-sm text-gray-900">{count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="bg-white shadow-sm rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <button className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
            Create Portfolio
          </button>
          <button className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
            Create Project
          </button>
          <button className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
            View Reports
          </button>
          <button className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
            Manage Users
          </button>
        </div>
      </div>
    </div>
  );
};