import React, { useState } from 'react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import { ClockIcon, UserIcon, FlagIcon } from '@heroicons/react/24/outline';
import { ProjectDetail } from '../../types/project';
import { projectService } from '../../services/projectService';

interface ProjectKanbanProps {
  projectDetail: ProjectDetail;
  onUpdate: () => void;
}

interface TaskCard {
  id: string;
  name: string;
  description?: string;
  priority: string;
  status: string;
  estimated_hours?: number;
  percent_complete: number;
  labels?: string[];
  assigned_to?: string;
  due_date?: string;
}

export const ProjectKanban: React.FC<ProjectKanbanProps> = ({ projectDetail, onUpdate }) => {
  const { tasks } = projectDetail;
  const [draggedTask, setDraggedTask] = useState<string | null>(null);
  const [isUpdating, setIsUpdating] = useState(false);

  const columns = [
    { id: 'not_started', title: 'To Do', color: 'bg-gray-100', textColor: 'text-gray-700' },
    { id: 'in_progress', title: 'In Progress', color: 'bg-blue-100', textColor: 'text-blue-700' },
    { id: 'completed', title: 'Done', color: 'bg-green-100', textColor: 'text-green-700' },
    { id: 'on_hold', title: 'On Hold', color: 'bg-yellow-100', textColor: 'text-yellow-700' }
  ];

  const getTasksForStatus = (status: string) => {
    return tasks.filter(task => task.status === status);
  };

  const handleDragStart = (result: any) => {
    setDraggedTask(result.draggableId);
  };

  const handleDragEnd = async (result: any) => {
    setDraggedTask(null);
    
    if (!result.destination) {
      return;
    }

    const taskId = result.draggableId;
    const newStatus = result.destination.droppableId;
    
    // Find the task that was moved
    const task = tasks.find(t => t.id === taskId);
    if (!task || task.status === newStatus) {
      return;
    }

    try {
      setIsUpdating(true);
      
      // Update task status
      await projectService.updateTask(projectDetail.project.id, taskId, {
        status: newStatus,
        ...(newStatus === 'completed' && { percent_complete: 100 }),
        ...(newStatus === 'in_progress' && task.percent_complete === 0 && { percent_complete: 10 }),
      });

      // Refresh project data
      onUpdate();
    } catch (error) {
      console.error('Failed to update task status:', error);
      // Could add toast notification here
    } finally {
      setIsUpdating(false);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority?.toLowerCase()) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-blue-100 text-blue-800 border-blue-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="space-y-6" data-testid="project-kanban">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-gray-900">Kanban Board</h2>
        <div className="flex space-x-3">
          {isUpdating && (
            <div className="flex items-center text-sm text-gray-500">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600 mr-2"></div>
              Updating...
            </div>
          )}
          <button className="btn btn-primary">Add Task</button>
        </div>
      </div>

      {/* Kanban Board with Drag & Drop */}
      <DragDropContext onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
        <div className="flex space-x-6 overflow-x-auto pb-4">
          {columns.map((column) => {
            const columnTasks = getTasksForStatus(column.id);
            
            return (
              <div key={column.id} className="flex-shrink-0 w-80">
                <div className={`${column.color} rounded-lg p-4 mb-4 border-2 border-transparent`}>
                  <div className="flex justify-between items-center">
                    <h3 className={`font-semibold ${column.textColor}`}>{column.title}</h3>
                    <span className="bg-white px-3 py-1 rounded-full text-sm font-medium text-gray-700 shadow-sm">
                      {columnTasks.length}
                    </span>
                  </div>
                </div>

                <Droppable droppableId={column.id}>
                  {(provided, snapshot) => (
                    <div
                      ref={provided.innerRef}
                      {...provided.droppableProps}
                      className={`space-y-3 min-h-[400px] p-2 rounded-lg transition-colors ${
                        snapshot.isDraggingOver ? 'bg-gray-50 ring-2 ring-primary-200' : ''
                      }`}
                    >
                      {columnTasks.map((task, index) => (
                        <Draggable key={task.id} draggableId={task.id} index={index}>
                          {(provided, snapshot) => (
                            <div
                              ref={provided.innerRef}
                              {...provided.draggableProps}
                              {...provided.dragHandleProps}
                              className={`bg-white rounded-lg shadow-sm p-4 border border-gray-200 cursor-pointer transition-all ${
                                snapshot.isDragging 
                                  ? 'shadow-lg ring-2 ring-primary-300 rotate-2' 
                                  : 'hover:shadow-md hover:border-gray-300'
                              } ${draggedTask === task.id ? 'opacity-50' : ''}`}
                            >
                              {/* Task Header */}
                              <div className="flex justify-between items-start mb-2">
                                <h4 className="font-medium text-gray-900 text-sm leading-tight flex-1 mr-2">
                                  {task.name}
                                </h4>
                                <span className={`px-2 py-0.5 rounded-full text-xs font-medium border ${getPriorityColor(task.priority)}`}>
                                  {task.priority?.toUpperCase()}
                                </span>
                              </div>
                              
                              {task.description && (
                                <p className="text-xs text-gray-600 mb-3 line-clamp-2 leading-relaxed">
                                  {task.description}
                                </p>
                              )}

                              {/* Task Metadata */}
                              <div className="flex items-center justify-between text-xs text-gray-500 mb-2">
                                {task.estimated_hours && (
                                  <div className="flex items-center">
                                    <ClockIcon className="h-3 w-3 mr-1" />
                                    <span>{task.estimated_hours}h</span>
                                  </div>
                                )}
                                
                                {task.assigned_to && (
                                  <div className="flex items-center">
                                    <UserIcon className="h-3 w-3 mr-1" />
                                    <span className="truncate max-w-[80px]">{task.assigned_to}</span>
                                  </div>
                                )}
                              </div>

                              {/* Progress Bar */}
                              <div className="mb-3">
                                <div className="flex justify-between text-xs mb-1">
                                  <span className="text-gray-600">Progress</span>
                                  <span className="font-medium text-gray-700">{Math.round(task.percent_complete)}%</span>
                                </div>
                                <div className="w-full bg-gray-200 rounded-full h-1.5">
                                  <div
                                    className={`h-1.5 rounded-full transition-all duration-300 ${
                                      task.percent_complete === 100 
                                        ? 'bg-green-500' 
                                        : task.percent_complete > 0 
                                        ? 'bg-blue-500' 
                                        : 'bg-gray-300'
                                    }`}
                                    style={{ width: `${Math.max(task.percent_complete, 0)}%` }}
                                  ></div>
                                </div>
                              </div>

                              {/* Labels */}
                              {task.labels && task.labels.length > 0 && (
                                <div className="flex flex-wrap gap-1">
                                  {task.labels.slice(0, 2).map((label) => (
                                    <span
                                      key={label}
                                      className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-primary-50 text-primary-700 border border-primary-200"
                                    >
                                      {label}
                                    </span>
                                  ))}
                                  {task.labels.length > 2 && (
                                    <span className="text-xs text-gray-500 px-1">+{task.labels.length - 2}</span>
                                  )}
                                </div>
                              )}
                            </div>
                          )}
                        </Draggable>
                      ))}
                      
                      {provided.placeholder}
                      
                      {/* Add Task Card */}
                      <button 
                        className="w-full border-2 border-dashed border-gray-300 rounded-lg p-4 text-gray-500 hover:border-gray-400 hover:text-gray-600 hover:bg-gray-50 transition-all"
                        onClick={() => {/* TODO: Open add task modal */}}
                      >
                        <div className="flex items-center justify-center">
                          <span className="text-lg mr-2">+</span>
                          <span>Add a task</span>
                        </div>
                      </button>
                    </div>
                  )}
                </Droppable>
              </div>
            );
          })}
        </div>
      </DragDropContext>

      {/* Board Stats */}
      <div className="bg-white rounded-lg shadow p-4">
        <h3 className="text-lg font-medium text-gray-900 mb-3">Board Summary</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {columns.map((column) => {
            const count = getTasksForStatus(column.id).length;
            return (
              <div key={column.id} className="text-center">
                <div className={`${column.color} rounded-lg p-3 mb-2`}>
                  <div className="text-2xl font-bold text-gray-900">{count}</div>
                </div>
                <div className="text-sm text-gray-600">{column.title}</div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};