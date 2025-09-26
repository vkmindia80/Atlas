import React from 'react';
import { ProjectDetail } from '../../types/project';

interface ProjectTasksProps {
  projectDetail: ProjectDetail;
  onUpdate: () => void;
}

export const ProjectTasks: React.FC<ProjectTasksProps> = ({ projectDetail }) => {
  const { tasks, task_summary } = projectDetail;

  return (
    <div className="space-y-6" data-testid="project-tasks">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-gray-900">Tasks</h2>
        <button className="btn btn-primary">Add Task</button>
      </div>

      {/* Task Summary */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="text-2xl font-bold text-gray-900">{task_summary.total}</div>
          <div className="text-sm text-gray-600">Total Tasks</div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="text-2xl font-bold text-blue-600">{task_summary.in_progress}</div>
          <div className="text-sm text-gray-600">In Progress</div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="text-2xl font-bold text-green-600">{task_summary.completed}</div>
          <div className="text-sm text-gray-600">Completed</div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="text-2xl font-bold text-yellow-600">{task_summary.not_started}</div>
          <div className="text-sm text-gray-600">Not Started</div>
        </div>
      </div>

      {/* Tasks List */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Task List</h3>
        </div>
        {tasks.length === 0 ? (
          <div className="p-6 text-center text-gray-500">
            No tasks found. Add your first task to get started.
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {tasks.slice(0, 10).map((task) => (
              <div key={task.id} className="p-4 hover:bg-gray-50">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900">{task.name}</h4>
                    {task.description && (
                      <p className="text-sm text-gray-600 mt-1">{task.description}</p>
                    )}
                    <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                      <span>Status: {task.status.replace('_', ' ')}</span>
                      <span>Priority: {task.priority}</span>
                      {task.estimated_hours && <span>Est: {task.estimated_hours}h</span>}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                      task.status === 'completed' ? 'bg-green-100 text-green-800' :
                      task.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                      task.status === 'on_hold' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {task.status.replace('_', ' ')}
                    </div>
                    <div className="text-sm text-gray-600 mt-1">
                      {task.percent_complete.toFixed(0)}%
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};