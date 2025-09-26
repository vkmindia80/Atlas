import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Tab } from '@headlessui/react';
import {
  CalendarIcon,
  ChartBarIcon,
  ExclamationTriangleIcon,
  DocumentIcon,
  CurrencyDollarIcon,
  UserGroupIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import { projectService } from '../../services/projectService';
import { ProjectDetail as ProjectDetailType } from '../../types/project';
import { ProjectOverview } from './ProjectOverview';
import { ProjectTasks } from './ProjectTasks';
import { ProjectGantt } from './ProjectGantt';
import { ProjectKanban } from './ProjectKanban';
import { ProjectCalendar } from './ProjectCalendar';
import { ProjectBudget } from './ProjectBudget';
import { ProjectRisks } from './ProjectRisks';
import { ProjectDocuments } from './ProjectDocuments';
import { QuickAddTask } from './QuickAddTask';

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(' ');
}

export const ProjectDetail: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
  const [projectDetail, setProjectDetail] = useState<ProjectDetailType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTab, setSelectedTab] = useState(0);

  const fetchProjectDetail = async () => {
    if (!projectId) return;
    
    try {
      setLoading(true);
      const data = await projectService.getProjectDetail(projectId);
      setProjectDetail(data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load project details');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjectDetail();
  }, [projectId]);

  const tabs = [
    { name: 'Overview', icon: ChartBarIcon, component: ProjectOverview },
    { name: 'Tasks', icon: ClockIcon, component: ProjectTasks },
    { name: 'Gantt', icon: CalendarIcon, component: ProjectGantt },
    { name: 'Board', icon: UserGroupIcon, component: ProjectKanban },
    { name: 'Calendar', icon: CalendarIcon, component: ProjectCalendar },
    { name: 'Budget', icon: CurrencyDollarIcon, component: ProjectBudget },
    { name: 'Risks', icon: ExclamationTriangleIcon, component: ProjectRisks },
    { name: 'Documents', icon: DocumentIcon, component: ProjectDocuments }
  ];

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error || !projectDetail) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <ExclamationTriangleIcon className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Error Loading Project</h3>
          <p className="text-gray-600 mb-4">{error}</p>
          <button onClick={fetchProjectDetail} className="btn btn-primary">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const { project } = projectDetail;

  return (
    <div className="min-h-screen bg-gray-50" data-testid="project-detail">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link
                to="/projects"
                className="text-gray-500 hover:text-gray-700"
                data-testid="back-to-projects"
              >
                ← Back to Projects
              </Link>
              <div>
                <h1 className="text-2xl font-bold text-gray-900" data-testid="project-name">
                  {project.name}
                </h1>
                <div className="flex items-center space-x-4 mt-1">
                  <span className="text-sm text-gray-600">{project.code}</span>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    project.status === 'active' ? 'bg-green-100 text-green-800' :
                    project.status === 'on_hold' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {project.status.replace('_', ' ').toUpperCase()}
                  </span>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    project.health_status === 'green' ? 'bg-green-100 text-green-800' :
                    project.health_status === 'yellow' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {project.health_status.toUpperCase()}
                  </span>
                </div>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="flex items-center space-x-6 text-sm text-gray-600">
              <div className="text-center">
                <div className="text-lg font-semibold text-gray-900">{project.percent_complete.toFixed(0)}%</div>
                <div>Complete</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold text-gray-900">{projectDetail.task_summary.total}</div>
                <div>Tasks</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold text-gray-900">{project.team_size}</div>
                <div>Team</div>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <Tab.Group selectedIndex={selectedTab} onChange={setSelectedTab}>
          <Tab.List className="flex space-x-8 px-6">
            {tabs.map((tab, index) => {
              const IconComponent = tab.icon;
              return (
                <Tab
                  key={tab.name}
                  className={({ selected }) =>
                    classNames(
                      'flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm',
                      selected
                        ? 'border-primary-500 text-primary-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    )
                  }
                  data-testid={`tab-${tab.name.toLowerCase()}`}
                >
                  <IconComponent className="h-5 w-5" />
                  <span>{tab.name}</span>
                </Tab>
              );
            })}
          </Tab.List>
        </Tab.Group>
      </div>

      {/* Tab Content */}
      <div className="flex-1">
        <Tab.Group selectedIndex={selectedTab} onChange={setSelectedTab}>
          <Tab.Panels>
            {tabs.map((tab, index) => {
              const ComponentToRender = tab.component;
              return (
                <Tab.Panel key={tab.name} className="p-6">
                  <ComponentToRender
                    projectDetail={projectDetail}
                    onUpdate={fetchProjectDetail}
                  />
                </Tab.Panel>
              );
            })}
          </Tab.Panels>
        </Tab.Group>
      </div>

      {/* Floating Action Button */}
      <QuickAddTask
        projectId={project.id}
        onTaskAdded={fetchProjectDetail}
      />
    </div>
  );
};