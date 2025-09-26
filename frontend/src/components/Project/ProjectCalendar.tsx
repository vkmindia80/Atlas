import React, { useState, useEffect } from 'react';
import { CalendarIcon, ClockIcon, UserIcon } from '@heroicons/react/24/outline';
import { ProjectDetail } from '../../types/project';

interface ProjectCalendarProps {
  projectDetail: ProjectDetail;
  onUpdate: () => void;
}

export const ProjectCalendar: React.FC<ProjectCalendarProps> = ({
  projectDetail,
  onUpdate
}) => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [viewMode, setViewMode] = useState<'month' | 'week'>('month');

  // Generate calendar grid
  const generateCalendar = () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startDate = new Date(firstDay);
    startDate.setDate(startDate.getDate() - firstDay.getDay());
    
    const days = [];
    const currentDateCalc = new Date(startDate);
    
    for (let i = 0; i < 42; i++) {
      days.push(new Date(currentDateCalc));
      currentDateCalc.setDate(currentDateCalc.getDate() + 1);
    }
    
    return days;
  };

  const calendarDays = generateCalendar();
  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  const navigateMonth = (direction: 'prev' | 'next') => {
    const newDate = new Date(currentDate);
    newDate.setMonth(newDate.getMonth() + (direction === 'next' ? 1 : -1));
    setCurrentDate(newDate);
  };

  // Mock events for demonstration
  const getEventsForDate = (date: Date) => {
    const events = [];
    const dateStr = date.toISOString().split('T')[0];
    
    // Add project milestone events
    if (projectDetail.milestones) {
      projectDetail.milestones.forEach(milestone => {
        if (milestone.planned_date === dateStr) {
          events.push({
            id: milestone.id,
            title: milestone.name,
            type: 'milestone',
            time: '09:00'
          });
        }
      });
    }
    
    // Add some sample task deadlines
    if (Math.random() > 0.8) {
      events.push({
        id: `task-${date.getDate()}`,
        title: 'Task Deadline',
        type: 'task',
        time: '17:00'
      });
    }
    
    return events;
  };

  return (
    <div className="bg-white rounded-lg shadow" data-testid="project-calendar">
      {/* Calendar Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h2 className="text-lg font-medium text-gray-900">Project Calendar</h2>
            <div className="flex rounded-md shadow-sm">
              <button
                onClick={() => setViewMode('month')}
                className={`px-3 py-1 text-sm font-medium rounded-l-md border ${
                  viewMode === 'month'
                    ? 'bg-primary-600 text-white border-primary-600'
                    : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                }`}
                data-testid="month-view-button"
              >
                Month
              </button>
              <button
                onClick={() => setViewMode('week')}
                className={`px-3 py-1 text-sm font-medium rounded-r-md border-t border-r border-b ${
                  viewMode === 'week'
                    ? 'bg-primary-600 text-white border-primary-600'
                    : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                }`}
                data-testid="week-view-button"
              >
                Week
              </button>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={() => navigateMonth('prev')}
              className="p-2 text-gray-400 hover:text-gray-600"
              data-testid="prev-month"
            >
              ←
            </button>
            <h3 className="text-lg font-semibold text-gray-900 min-w-[200px] text-center">
              {monthNames[currentDate.getMonth()]} {currentDate.getFullYear()}
            </h3>
            <button
              onClick={() => navigateMonth('next')}
              className="p-2 text-gray-400 hover:text-gray-600"
              data-testid="next-month"
            >
              →
            </button>
          </div>
        </div>
      </div>

      {/* Calendar Grid */}
      <div className="p-6">
        {/* Days of week header */}
        <div className="grid grid-cols-7 gap-1 mb-4">
          {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
            <div key={day} className="p-2 text-center text-sm font-medium text-gray-500">
              {day}
            </div>
          ))}
        </div>

        {/* Calendar days */}
        <div className="grid grid-cols-7 gap-1">
          {calendarDays.map((day, index) => {
            const isCurrentMonth = day.getMonth() === currentDate.getMonth();
            const isToday = day.toDateString() === new Date().toDateString();
            const events = getEventsForDate(day);

            return (
              <div
                key={index}
                className={`min-h-[80px] p-2 border border-gray-200 ${
                  isCurrentMonth ? 'bg-white' : 'bg-gray-50'
                } ${isToday ? 'ring-2 ring-primary-500' : ''}`}
                data-testid={`calendar-day-${day.getDate()}`}
              >
                <div className={`text-sm ${
                  isCurrentMonth ? 'text-gray-900' : 'text-gray-400'
                } ${isToday ? 'font-bold' : ''}`}>
                  {day.getDate()}
                </div>
                
                {/* Events */}
                <div className="mt-1 space-y-1">
                  {events.slice(0, 2).map(event => (
                    <div
                      key={event.id}
                      className={`text-xs p-1 rounded truncate ${
                        event.type === 'milestone'
                          ? 'bg-purple-100 text-purple-800'
                          : 'bg-blue-100 text-blue-800'
                      }`}
                      title={`${event.title} at ${event.time}`}
                    >
                      {event.title}
                    </div>
                  ))}
                  {events.length > 2 && (
                    <div className="text-xs text-gray-500">
                      +{events.length - 2} more
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Legend */}
      <div className="px-6 py-4 border-t border-gray-200 bg-gray-50">
        <div className="flex items-center space-x-6 text-sm">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded bg-purple-500"></div>
            <span className="text-gray-600">Milestones</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded bg-blue-500"></div>
            <span className="text-gray-600">Task Deadlines</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded bg-green-500"></div>
            <span className="text-gray-600">Project Phases</span>
          </div>
        </div>
      </div>
    </div>
  );
};