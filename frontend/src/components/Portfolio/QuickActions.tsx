import React, { useState } from 'react';
import { PlusIcon, DocumentArrowUpIcon, ChartBarIcon, CogIcon } from '@heroicons/react/24/outline';

interface QuickActionsProps {
  portfolioId: string;
}

export const QuickActions: React.FC<QuickActionsProps> = ({ portfolioId }) => {
  const [isOpen, setIsOpen] = useState(false);

  const actions = [
    {
      icon: PlusIcon,
      label: 'Add Project',
      action: () => {
        // Navigate to add project form
        console.log('Add project to portfolio:', portfolioId);
      }
    },
    {
      icon: DocumentArrowUpIcon,
      label: 'Import Projects',
      action: () => {
        // Open import dialog
        console.log('Import projects to portfolio:', portfolioId);
      }
    },
    {
      icon: ChartBarIcon,
      label: 'Generate Report',
      action: () => {
        // Generate portfolio report
        console.log('Generate report for portfolio:', portfolioId);
      }
    },
    {
      icon: CogIcon,
      label: 'Portfolio Settings',
      action: () => {
        // Open portfolio settings
        console.log('Open settings for portfolio:', portfolioId);
      }
    }
  ];

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="btn btn-primary flex items-center space-x-2"
        data-testid="quick-actions-btn"
      >
        <PlusIcon className="h-5 w-5" />
        <span>Actions</span>
      </button>

      {isOpen && (
        <>
          {/* Overlay */}
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          ></div>
          
          {/* Dropdown */}
          <div className="absolute right-0 mt-2 w-56 bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 z-20">
            <div className="py-1">
              {actions.map((action, index) => {
                const IconComponent = action.icon;
                return (
                  <button
                    key={index}
                    onClick={() => {
                      action.action();
                      setIsOpen(false);
                    }}
                    className="flex items-center space-x-3 w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                    data-testid={`quick-action-${index}`}
                  >
                    <IconComponent className="h-5 w-5" />
                    <span>{action.label}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </>
      )}
    </div>
  );
};