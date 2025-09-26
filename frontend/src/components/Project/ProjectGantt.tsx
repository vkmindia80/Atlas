import React from 'react';
import { ProjectDetail } from '../../types/project';

interface ProjectGanttProps {
  projectDetail: ProjectDetail;
  onUpdate: () => void;
}

export const ProjectGantt: React.FC<ProjectGanttProps> = ({ projectDetail }) => {
  const { project, tasks, milestones } = projectDetail;

  return (
    <div className="space-y-6" data-testid="project-gantt">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-gray-900">Gantt Chart</h2>
        <div className="flex space-x-2">
          <button className="btn btn-secondary">Export</button>
          <button className="btn btn-primary">Add Dependency</button>
        </div>
      </div>

      {/* Gantt Chart Placeholder */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Interactive Gantt Chart</h3>
          <p className="text-gray-600 mb-4">
            Visualize project timeline, dependencies, and critical path
          </p>
          <div className="text-sm text-gray-500">
            • {tasks.length} tasks scheduled
            • {milestones.length} milestones defined
            • Drag and drop support
            • Real-time dependency management
          </div>
        </div>
      </div>

      {/* Timeline Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Project Timeline</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Start Date</span>
              <span className="font-medium">
                {project.planned_start_date ? new Date(project.planned_start_date).toLocaleDateString() : 'Not set'}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">End Date</span>
              <span className="font-medium">
                {project.planned_end_date ? new Date(project.planned_end_date).toLocaleDateString() : 'Not set'}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Duration</span>
              <span className="font-medium">
                {project.planned_start_date && project.planned_end_date
                  ? `${Math.ceil((new Date(project.planned_end_date).getTime() - new Date(project.planned_start_date).getTime()) / (1000 * 60 * 60 * 24))} days`
                  : 'Not calculated'}
              </span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Upcoming Milestones</h3>
          {milestones.length === 0 ? (
            <p className="text-gray-500">No milestones defined</p>
          ) : (
            <div className="space-y-3">
              {milestones.slice(0, 3).map((milestone) => (
                <div key={milestone.id} className="flex justify-between items-center">
                  <div>
                    <div className="font-medium text-sm">{milestone.name}</div>
                    <div className="text-xs text-gray-500">
                      {new Date(milestone.planned_date).toLocaleDateString()}
                    </div>
                  </div>
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                    milestone.status === 'completed' ? 'bg-green-100 text-green-800' :
                    milestone.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {milestone.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};