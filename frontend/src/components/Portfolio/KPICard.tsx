import React from 'react';
import { IconType } from 'react-icons';

interface KPICardProps {
  title: string;
  value: string | number;
  icon: any; // Heroicon component
  color: 'blue' | 'green' | 'yellow' | 'red' | 'indigo' | 'purple';
  subtitle?: string;
  trend?: {
    value: number;
    direction: 'up' | 'down';
  };
  'data-testid'?: string;
}

const colorClasses = {
  blue: 'bg-blue-50 text-blue-600',
  green: 'bg-green-50 text-green-600',
  yellow: 'bg-yellow-50 text-yellow-600',
  red: 'bg-red-50 text-red-600',
  indigo: 'bg-indigo-50 text-indigo-600',
  purple: 'bg-purple-50 text-purple-600',
};

export const KPICard: React.FC<KPICardProps> = ({
  title,
  value,
  icon: Icon,
  color,
  subtitle,
  trend,
  'data-testid': testId
}) => {
  return (
    <div 
      className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow"
      data-testid={testId}
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-3xl font-semibold text-gray-900 mt-1" data-testid={`${testId}-value`}>
            {value}
          </p>
          {subtitle && (
            <p className="text-sm text-gray-500 mt-1">{subtitle}</p>
          )}
          {trend && (
            <div className={`flex items-center mt-2 ${
              trend.direction === 'up' ? 'text-green-600' : 'text-red-600'
            }`}>
              <svg
                className={`w-4 h-4 mr-1 ${
                  trend.direction === 'up' ? 'rotate-0' : 'rotate-180'
                }`}
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z"
                  clipRule="evenodd"
                />
              </svg>
              <span className="text-sm font-medium">{Math.abs(trend.value)}%</span>
            </div>
          )}
        </div>
        <div className={`p-3 rounded-full ${colorClasses[color]}`}>
          <Icon className="h-6 w-6" />
        </div>
      </div>
    </div>
  );
};