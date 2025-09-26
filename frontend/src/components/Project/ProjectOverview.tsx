import React from 'react';
import {
  CalendarIcon,
  UserIcon,
  CurrencyDollarIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { ProjectDetail } from '../../types/project';

interface ProjectOverviewProps {
  projectDetail: ProjectDetail;
  onUpdate: () => void;
}

export const ProjectOverview: React.FC<ProjectOverviewProps> = ({ projectDetail }) => {
  const { project, task_summary, milestones, risks, issues } = projectDetail;

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  const getProgressColor = (percentage: number) => {
    if (percentage >= 90) return 'bg-green-500';
    if (percentage >= 70) return 'bg-blue-500';
    if (percentage >= 50) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const upcomingMilestones = milestones
    .filter(m => m.status === 'planned' || m.status === 'in_progress')
    .sort((a, b) => new Date(a.planned_date).getTime() - new Date(b.planned_date).getTime())
    .slice(0, 3);

  const activeRisks = risks.filter(r => r.status === 'active');
  const openIssues = issues.filter(i => i.status === 'active');

  return (
    <div className="space-y-6" data-testid="project-overview">
      {/* Project Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Project Progress */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-medium text-gray-900">Project Progress</h3>
            <CheckCircleIcon className="h-6 w-6 text-green-500" />
          </div>
          <div className="mb-4">
            <div className="flex justify-between text-sm mb-2">
              <span>Overall Progress</span>
              <span className="font-semibold">{project.percent_complete.toFixed(0)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className={`h-3 rounded-full ${getProgressColor(project.percent_complete)}`}
                style={{ width: `${project.percent_complete}%` }}
              ></div>
            </div>
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">Tasks Complete</span>
              <span className="font-medium">{task_summary.completed} / {task_summary.total}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">In Progress</span>
              <span className="font-medium">{task_summary.in_progress}</span>
            </div>
          </div>
        </div>

        {/* Timeline */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-medium text-gray-900">Timeline</h3>
            <CalendarIcon className="h-6 w-6 text-blue-500" />
          </div>
          <div className="space-y-3 text-sm">
            <div>
              <span className="text-gray-600">Start Date</span>
              <div className="font-medium">
                {project.planned_start_date ? formatDate(project.planned_start_date) : 'Not set'}
              </div>
            </div>
            <div>
              <span className="text-gray-600">End Date</span>
              <div className="font-medium">
                {project.planned_end_date ? formatDate(project.planned_end_date) : 'Not set'}
              </div>
            </div>
            {project.actual_start_date && (
              <div>
                <span className="text-gray-600">Actual Start</span>
                <div className="font-medium">{formatDate(project.actual_start_date)}</div>
              </div>
            )}
          </div>
        </div>

        {/* Budget */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-medium text-gray-900">Budget</h3>
            <CurrencyDollarIcon className="h-6 w-6 text-green-500" />
          </div>
          <div className="space-y-3 text-sm">
            <div>
              <span className="text-gray-600">Total Budget</span>
              <div className="font-medium text-lg">
                {formatCurrency(project.financials.total_budget)}
              </div>
            </div>
            <div>
              <span className="text-gray-600">Spent</span>
              <div className="font-medium">
                {formatCurrency(project.financials.spent_amount)}
              </div>
            </div>
            <div className="pt-2 border-t">
              <div className="flex justify-between">
                <span className="text-gray-600">Remaining</span>
                <span className="font-medium text-green-600">
                  {formatCurrency(project.financials.total_budget - project.financials.spent_amount)}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Detailed Sections */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Upcoming Milestones */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Upcoming Milestones</h3>
          {upcomingMilestones.length === 0 ? (
            <p className="text-gray-500">No upcoming milestones</p>
          ) : (
            <div className="space-y-3">
              {upcomingMilestones.map((milestone) => (
                <div key={milestone.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                  <div>
                    <div className="font-medium text-sm">{milestone.name}</div>
                    <div className="text-xs text-gray-600">
                      Due: {formatDate(milestone.planned_date)}
                    </div>
                  </div>
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                    milestone.status === 'completed' ? 'bg-green-100 text-green-800' :
                    milestone.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {milestone.status.replace('_', ' ')}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Risks & Issues Summary */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Risks & Issues</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />
                <span className="text-sm font-medium">Active Risks</span>
              </div>
              <span className="text-lg font-bold text-red-600">{activeRisks.length}</span>
            </div>
            
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500" />
                <span className="text-sm font-medium">Open Issues</span>
              </div>
              <span className="text-lg font-bold text-yellow-600">{openIssues.length}</span>
            </div>

            {(activeRisks.length > 0 || openIssues.length > 0) && (
              <div className="pt-3 border-t">
                <div className="text-xs text-gray-600">
                  Risk Score: {(project.risk_score * 100).toFixed(0)}%
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                  <div
                    className={`h-2 rounded-full ${
                      project.risk_score > 0.7 ? 'bg-red-500' :
                      project.risk_score > 0.4 ? 'bg-yellow-500' : 'bg-green-500'
                    }`}
                    style={{ width: `${project.risk_score * 100}%` }}
                  ></div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Project Description */}
      {project.description && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Description</h3>
          <p className="text-gray-700">{project.description}</p>
        </div>
      )}
    </div>
  );
};