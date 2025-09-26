import React from 'react';
import { ProjectDetail } from '../../types/project';

interface ProjectKanbanProps {
  projectDetail: ProjectDetail;
  onUpdate: () => void;
}

export const ProjectKanban: React.FC<ProjectKanbanProps> = ({ projectDetail }) => {
  const { tasks } = projectDetail;

  const columns = [
    { id: 'not_started', title: 'To Do', color: 'bg-gray-100' },
    { id: 'in_progress', title: 'In Progress', color: 'bg-blue-100' },
    { id: 'completed', title: 'Done', color: 'bg-green-100' },
    { id: 'on_hold', title: 'On Hold', color: 'bg-yellow-100' }
  ];

  const getTasksForStatus = (status: string) => {
    return tasks.filter(task => task.status === status);
  };

  return (
    <div className="space-y-6" data-testid="project-kanban">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-gray-900">Kanban Board</h2>
        <button className="btn btn-primary">Add Task</button>
      </div>

      {/* Kanban Board */}
      <div className="flex space-x-6 overflow-x-auto pb-4">
        {columns.map((column) => {
          const columnTasks = getTasksForStatus(column.id);
          
          return (
            <div key={column.id} className="flex-shrink-0 w-80">
              <div className={`${column.color} rounded-lg p-4 mb-4`}>
                <div className="flex justify-between items-center">
                  <h3 className="font-semibold text-gray-900">{column.title}</h3>
                  <span className="bg-white px-2 py-1 rounded-full text-sm font-medium text-gray-700">
                    {columnTasks.length}
                  </span>
                </div>
              </div>

              {/* Task Cards */}
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {columnTasks.map((task) => (
                  <div
                    key={task.id}
                    className="bg-white rounded-lg shadow p-4 border border-gray-200 hover:shadow-md transition-shadow cursor-pointer"
                  >
                    <h4 className="font-medium text-gray-900 mb-2">{task.name}</h4>
                    
                    {task.description && (
                      <p className="text-sm text-gray-600 mb-3 line-clamp-2">{task.description}</p>
                    )}

                    <div className="flex justify-between items-center text-xs text-gray-500">
                      <span className={`px-2 py-1 rounded-full ${
                        task.priority === 'high' ? 'bg-red-100 text-red-800' :
                        task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {task.priority}
                      </span>
                      
                      {task.estimated_hours && (
                        <span>{task.estimated_hours}h</span>
                      )}
                    </div>

                    {/* Progress Bar */}
                    <div className="mt-3">
                      <div className="flex justify-between text-xs mb-1">
                        <span>Progress</span>
                        <span>{task.percent_complete.toFixed(0)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full"
                          style={{ width: `${task.percent_complete}%` }}
                        ></div>
                      </div>
                    </div>

                    {/* Labels */}
                    {task.labels && task.labels.length > 0 && (
                      <div className="mt-3 flex flex-wrap gap-1">
                        {task.labels.slice(0, 3).map((label) => (
                          <span
                            key={label}
                            className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800"
                          >
                            {label}
                          </span>
                        ))}
                        {task.labels.length > 3 && (
                          <span className="text-xs text-gray-500">+{task.labels.length - 3}</span>
                        )}
                      </div>
                    )}
                  </div>
                ))}

                {/* Add Task Card */}
                <button className="w-full border-2 border-dashed border-gray-300 rounded-lg p-4 text-gray-500 hover:border-gray-400 hover:text-gray-600 transition-colors">
                  + Add a task
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};