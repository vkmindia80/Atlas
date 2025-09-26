import React, { useState } from 'react';
import { PlusIcon } from '@heroicons/react/24/outline';
import { projectService } from '../../services/projectService';

interface QuickAddTaskProps {
  projectId: string;
  onTaskAdded: () => void;
}

export const QuickAddTask: React.FC<QuickAddTaskProps> = ({ projectId, onTaskAdded }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [taskName, setTaskName] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!taskName.trim()) return;

    try {
      setLoading(true);
      await projectService.createTask(projectId, {
        name: taskName.trim(),
        status: 'not_started',
        priority: 'medium',
        percent_complete: 0
      });
      
      setTaskName('');
      setIsOpen(false);
      onTaskAdded();
    } catch (error) {
      console.error('Error creating task:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Floating Action Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 bg-primary-600 hover:bg-primary-700 text-white rounded-full p-4 shadow-lg hover:shadow-xl transition-all z-50"
        data-testid="quick-add-task-btn"
      >
        <PlusIcon className="h-6 w-6" />
      </button>

      {/* Modal */}
      {isOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            {/* Backdrop */}
            <div
              className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
              onClick={() => setIsOpen(false)}
            ></div>

            {/* Modal Panel */}
            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
              <form onSubmit={handleSubmit}>
                <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                  <div className="sm:flex sm:items-start">
                    <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-primary-100 sm:mx-0 sm:h-10 sm:w-10">
                      <PlusIcon className="h-6 w-6 text-primary-600" />
                    </div>
                    <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left flex-1">
                      <h3 className="text-lg leading-6 font-medium text-gray-900">
                        Quick Add Task
                      </h3>
                      <div className="mt-4">
                        <input
                          type="text"
                          placeholder="Enter task name..."
                          value={taskName}
                          onChange={(e) => setTaskName(e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                          autoFocus
                          data-testid="quick-task-input"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                  <button
                    type="submit"
                    disabled={!taskName.trim() || loading}
                    className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                    data-testid="quick-task-submit"
                  >
                    {loading ? 'Adding...' : 'Add Task'}
                  </button>
                  <button
                    type="button"
                    onClick={() => setIsOpen(false)}
                    className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </>
  );
};