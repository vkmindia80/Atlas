import React, { useState, useEffect, useMemo } from 'react';
import { format, addDays, startOfWeek, endOfWeek, differenceInDays, parseISO, isValid } from 'date-fns';
import { ChevronLeftIcon, ChevronRightIcon, CalendarIcon, ClockIcon } from '@heroicons/react/24/outline';
import { ProjectDetail } from '../../types/project';

interface ProjectGanttProps {
  projectDetail: ProjectDetail;
  onUpdate: () => void;
}

export const ProjectGantt: React.FC<ProjectGanttProps> = ({ projectDetail, onUpdate }) => {
  const { project, tasks, milestones } = projectDetail;
  const [viewStart, setViewStart] = useState(new Date());
  const [viewMode, setViewMode] = useState<'week' | 'month'>('month');
  const [selectedTask, setSelectedTask] = useState<string | null>(null);

  // Calculate project date range
  const projectDateRange = useMemo(() => {
    const dates: Date[] = [];
    
    if (project.planned_start_date) {
      const startDate = parseISO(project.planned_start_date);
      if (isValid(startDate)) dates.push(startDate);
    }
    
    if (project.planned_end_date) {
      const endDate = parseISO(project.planned_end_date);
      if (isValid(endDate)) dates.push(endDate);
    }

    tasks.forEach(task => {
      if (task.planned_start_date) {
        const taskStart = parseISO(task.planned_start_date);
        if (isValid(taskStart)) dates.push(taskStart);
      }
      if (task.planned_end_date) {
        const taskEnd = parseISO(task.planned_end_date);
        if (isValid(taskEnd)) dates.push(taskEnd);
      }
    });

    if (dates.length === 0) {
      const today = new Date();
      return {
        start: startOfWeek(today),
        end: endOfWeek(addDays(today, 90))
      };
    }

    const sortedDates = dates.sort((a, b) => a.getTime() - b.getTime());
    return {
      start: startOfWeek(sortedDates[0]),
      end: endOfWeek(sortedDates[sortedDates.length - 1])
    };
  }, [project, tasks]);

  // Generate timeline columns
  const timelineColumns = useMemo(() => {
    const columns = [];
    const current = new Date(viewStart);
    const columnCount = viewMode === 'week' ? 12 : 8; // Show 12 weeks or 8 months
    
    for (let i = 0; i < columnCount; i++) {
      columns.push(new Date(current));
      if (viewMode === 'week') {
        current.setDate(current.getDate() + 7);
      } else {
        current.setMonth(current.getMonth() + 1);
      }
    }
    
    return columns;
  }, [viewStart, viewMode]);

  // Calculate task position and width
  const getTaskDimensions = (task: any) => {
    if (!task.planned_start_date || !task.planned_end_date) {
      return { left: 0, width: 0, visible: false };
    }

    const taskStart = parseISO(task.planned_start_date);
    const taskEnd = parseISO(task.planned_end_date);
    
    if (!isValid(taskStart) || !isValid(taskEnd)) {
      return { left: 0, width: 0, visible: false };
    }

    const viewEnd = new Date(timelineColumns[timelineColumns.length - 1]);
    viewEnd.setDate(viewEnd.getDate() + (viewMode === 'week' ? 7 : 30));

    // Check if task is visible in current view
    if (taskEnd < viewStart || taskStart > viewEnd) {
      return { left: 0, width: 0, visible: false };
    }

    const totalViewDays = differenceInDays(viewEnd, viewStart);
    const taskStartDays = Math.max(0, differenceInDays(taskStart, viewStart));
    const taskEndDays = Math.min(totalViewDays, differenceInDays(taskEnd, viewStart));
    const taskDurationDays = taskEndDays - taskStartDays;

    const left = (taskStartDays / totalViewDays) * 100;
    const width = (taskDurationDays / totalViewDays) * 100;

    return { left, width: Math.max(width, 1), visible: true };
  };

  const navigateView = (direction: 'prev' | 'next') => {
    const newDate = new Date(viewStart);
    if (viewMode === 'week') {
      newDate.setDate(newDate.getDate() + (direction === 'next' ? 7 : -7));
    } else {
      newDate.setMonth(newDate.getMonth() + (direction === 'next' ? 1 : -1));
    }
    setViewStart(newDate);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-500';
      case 'in_progress': return 'bg-blue-500';
      case 'on_hold': return 'bg-yellow-500';
      default: return 'bg-gray-400';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority?.toLowerCase()) {
      case 'high': return 'border-l-red-500';
      case 'medium': return 'border-l-yellow-500';
      case 'low': return 'border-l-blue-500';
      default: return 'border-l-gray-400';
    }
  };

  return (
    <div className="space-y-6" data-testid="project-gantt">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-gray-900">Gantt Chart</h2>
        <div className="flex space-x-2">
          <div className="flex rounded-md shadow-sm">
            <button
              onClick={() => setViewMode('week')}
              className={`px-3 py-2 text-sm font-medium rounded-l-md border ${
                viewMode === 'week'
                  ? 'bg-primary-600 text-white border-primary-600'
                  : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
              }`}
            >
              Week
            </button>
            <button
              onClick={() => setViewMode('month')}
              className={`px-3 py-2 text-sm font-medium rounded-r-md border-t border-r border-b ${
                viewMode === 'month'
                  ? 'bg-primary-600 text-white border-primary-600'
                  : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
              }`}
            >
              Month
            </button>
          </div>
          <button className="btn btn-secondary">Export</button>
          <button className="btn btn-primary">Add Task</button>
        </div>
      </div>

      {/* Gantt Chart */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {/* Timeline Header */}
        <div className="border-b border-gray-200">
          <div className="flex">
            {/* Task Names Column Header */}
            <div className="w-80 p-4 border-r border-gray-200 bg-gray-50">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-medium text-gray-900">Tasks ({tasks.length})</h3>
                <div className="flex space-x-1">
                  <button
                    onClick={() => navigateView('prev')}
                    className="p-1 text-gray-400 hover:text-gray-600"
                  >
                    <ChevronLeftIcon className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => navigateView('next')}
                    className="p-1 text-gray-400 hover:text-gray-600"
                  >
                    <ChevronRightIcon className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* Timeline Header */}
            <div className="flex-1 bg-gray-50">
              <div className="grid" style={{ gridTemplateColumns: `repeat(${timelineColumns.length}, 1fr)` }}>
                {timelineColumns.map((date, index) => (
                  <div key={index} className="p-2 border-r border-gray-200 text-center">
                    <div className="text-xs font-medium text-gray-900">
                      {viewMode === 'week' 
                        ? format(date, 'MMM dd') 
                        : format(date, 'MMM yyyy')
                      }
                    </div>
                    <div className="text-xs text-gray-500">
                      {viewMode === 'week' 
                        ? format(date, 'E') 
                        : format(date, 'MMM')
                      }
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Tasks List */}
        <div className="max-h-96 overflow-y-auto">
          {tasks.length === 0 ? (
            <div className="flex items-center justify-center py-12 text-gray-500">
              <div className="text-center">
                <CalendarIcon className="h-8 w-8 mx-auto mb-2 text-gray-400" />
                <p>No tasks scheduled</p>
              </div>
            </div>
          ) : (
            tasks.map((task) => {
              const dimensions = getTaskDimensions(task);
              
              return (
                <div key={task.id} className="flex border-b border-gray-100 hover:bg-gray-50">
                  {/* Task Info Column */}
                  <div className="w-80 p-3 border-r border-gray-200">
                    <div className="flex items-center space-x-2">
                      <div className={`w-1 h-8 rounded ${getPriorityColor(task.priority)}`}></div>
                      <div className="flex-1 min-w-0">
                        <h4 className="text-sm font-medium text-gray-900 truncate">
                          {task.name}
                        </h4>
                        <div className="flex items-center space-x-3 text-xs text-gray-500">
                          <span className={`inline-flex items-center px-2 py-0.5 rounded-full ${
                            task.status === 'completed' ? 'bg-green-100 text-green-800' :
                            task.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                            task.status === 'on_hold' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-gray-100 text-gray-800'
                          }`}>
                            {task.status?.replace('_', ' ')}
                          </span>
                          {task.estimated_hours && (
                            <div className="flex items-center">
                              <ClockIcon className="h-3 w-3 mr-1" />
                              {task.estimated_hours}h
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Timeline Column */}
                  <div className="flex-1 relative h-12 border-r border-gray-200">
                    {/* Background grid */}
                    <div className="absolute inset-0 grid" style={{ gridTemplateColumns: `repeat(${timelineColumns.length}, 1fr)` }}>
                      {timelineColumns.map((_, index) => (
                        <div key={index} className="border-r border-gray-100"></div>
                      ))}
                    </div>

                    {/* Task Bar */}
                    {dimensions.visible && (
                      <div
                        className={`absolute top-2 bottom-2 rounded ${getStatusColor(task.status)} ${
                          selectedTask === task.id ? 'ring-2 ring-primary-500' : ''
                        } cursor-pointer hover:opacity-80 transition-opacity`}
                        style={{
                          left: `${dimensions.left}%`,
                          width: `${dimensions.width}%`
                        }}
                        onClick={() => setSelectedTask(selectedTask === task.id ? null : task.id)}
                        title={`${task.name} (${Math.round(task.percent_complete)}% complete)`}
                      >
                        {/* Progress overlay */}
                        <div
                          className="absolute top-0 bottom-0 left-0 bg-black bg-opacity-20 rounded"
                          style={{ width: `${100 - task.percent_complete}%`, right: 0, left: 'auto' }}
                        ></div>
                        
                        {/* Task label (if wide enough) */}
                        {dimensions.width > 10 && (
                          <div className="absolute inset-0 flex items-center px-2">
                            <span className="text-white text-xs font-medium truncate">
                              {task.name}
                            </span>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              );
            })
          )}
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