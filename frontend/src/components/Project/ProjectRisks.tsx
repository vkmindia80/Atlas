import React, { useState } from 'react';
import { 
  ExclamationTriangleIcon, 
  PlusIcon, 
  ChartBarIcon,
  ClockIcon,
  UserIcon
} from '@heroicons/react/24/outline';
import { ProjectDetail } from '../../types/project';

interface ProjectRisksProps {
  projectDetail: ProjectDetail;
  onUpdate: () => void;
}

interface Risk {
  id: string;
  title: string;
  description: string;
  category: 'technical' | 'financial' | 'resource' | 'schedule' | 'external';
  probability: 'low' | 'medium' | 'high';
  impact: 'low' | 'medium' | 'high';
  status: 'open' | 'mitigated' | 'closed';
  owner: string;
  mitigation: string;
  createdAt: string;
  dueDate?: string;
}

interface Issue {
  id: string;
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'open' | 'in_progress' | 'resolved' | 'closed';
  assignee: string;
  createdAt: string;
  resolvedAt?: string;
}

export const ProjectRisks: React.FC<ProjectRisksProps> = ({
  projectDetail,
  onUpdate
}) => {
  const [activeTab, setActiveTab] = useState<'risks' | 'issues' | 'decisions'>('risks');
  const [showAddRisk, setShowAddRisk] = useState(false);
  const [showAddIssue, setShowAddIssue] = useState(false);

  // Mock data for demonstration
  const mockRisks: Risk[] = [
    {
      id: '1',
      title: 'Third-party API Dependency',
      description: 'External API service may have availability issues affecting project timeline',
      category: 'technical',
      probability: 'medium',
      impact: 'high',
      status: 'open',
      owner: 'John Doe',
      mitigation: 'Implement fallback mechanism and monitor API health',
      createdAt: '2024-01-15',
      dueDate: '2024-02-15'
    },
    {
      id: '2',
      title: 'Budget Overrun Risk',
      description: 'Current spending rate may exceed allocated budget by 15%',
      category: 'financial',
      probability: 'high',
      impact: 'medium',
      status: 'open',
      owner: 'Jane Smith',
      mitigation: 'Weekly budget reviews and scope adjustments',
      createdAt: '2024-01-10'
    },
    {
      id: '3',
      title: 'Key Resource Availability',
      description: 'Lead developer may not be available for final phase',
      category: 'resource',
      probability: 'low',
      impact: 'high',
      status: 'mitigated',
      owner: 'Mike Johnson',
      mitigation: 'Cross-trained backup developer and documented processes',
      createdAt: '2024-01-05'
    }
  ];

  const mockIssues: Issue[] = [
    {
      id: '1',
      title: 'Database Performance Bottleneck',
      description: 'Query response times exceeding 2 seconds under load testing',
      priority: 'high',
      status: 'in_progress',
      assignee: 'Alice Brown',
      createdAt: '2024-01-20'
    },
    {
      id: '2',
      title: 'UI Inconsistency',
      description: 'Navigation elements not following design system guidelines',
      priority: 'medium',
      status: 'open',
      assignee: 'Bob Wilson',
      createdAt: '2024-01-18'
    },
    {
      id: '3',
      title: 'Missing Test Coverage',
      description: 'Unit test coverage below 80% threshold',
      priority: 'medium',
      status: 'resolved',
      assignee: 'Carol Davis',
      createdAt: '2024-01-12',
      resolvedAt: '2024-01-19'
    }
  ];

  const getRiskScore = (probability: string, impact: string) => {
    const probValue = probability === 'high' ? 3 : probability === 'medium' ? 2 : 1;
    const impactValue = impact === 'high' ? 3 : impact === 'medium' ? 2 : 1;
    return probValue * impactValue;
  };

  const getRiskColor = (score: number) => {
    if (score >= 6) return 'bg-red-100 text-red-800 border-red-200';
    if (score >= 4) return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    return 'bg-green-100 text-green-800 border-green-200';
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return 'bg-red-100 text-red-800';
      case 'in_progress': return 'bg-blue-100 text-blue-800';
      case 'mitigated': 
      case 'resolved': return 'bg-green-100 text-green-800';
      case 'closed': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'bg-red-100 text-red-800';
      case 'high': return 'bg-orange-100 text-orange-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6" data-testid="project-risks">
      {/* Header with Stats */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-red-50 rounded-lg">
            <div className="text-2xl font-bold text-red-600" data-testid="open-risks-count">
              {mockRisks.filter(r => r.status === 'open').length}
            </div>
            <div className="text-sm text-gray-600">Open Risks</div>
          </div>
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600" data-testid="open-issues-count">
              {mockIssues.filter(i => i.status === 'open' || i.status === 'in_progress').length}
            </div>
            <div className="text-sm text-gray-600">Active Issues</div>
          </div>
          <div className="text-center p-4 bg-yellow-50 rounded-lg">
            <div className="text-2xl font-bold text-yellow-600">
              {mockRisks.filter(r => getRiskScore(r.probability, r.impact) >= 6).length}
            </div>
            <div className="text-sm text-gray-600">High Risk Items</div>
          </div>
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600">
              {mockRisks.filter(r => r.status === 'mitigated').length + mockIssues.filter(i => i.status === 'resolved').length}
            </div>
            <div className="text-sm text-gray-600">Resolved Items</div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8 px-6">
            {[
              { id: 'risks', name: 'Risks', count: mockRisks.length },
              { id: 'issues', name: 'Issues', count: mockIssues.length },
              { id: 'decisions', name: 'Decisions', count: 3 }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
                data-testid={`tab-${tab.id}`}
              >
                {tab.name} ({tab.count})
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'risks' && (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-medium text-gray-900">Risk Register</h3>
                <button
                  onClick={() => setShowAddRisk(true)}
                  className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
                  data-testid="add-risk-button"
                >
                  <PlusIcon className="h-4 w-4 mr-2" />
                  Add Risk
                </button>
              </div>

              <div className="space-y-3">
                {mockRisks.map((risk) => {
                  const riskScore = getRiskScore(risk.probability, risk.impact);
                  
                  return (
                    <div key={risk.id} className={`border rounded-lg p-4 ${getRiskColor(riskScore)}`}>
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <h4 className="font-medium text-gray-900">{risk.title}</h4>
                            <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(risk.status)}`}>
                              {risk.status.replace('_', ' ').toUpperCase()}
                            </span>
                            <span className="px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800">
                              {risk.category.toUpperCase()}
                            </span>
                          </div>
                          
                          <p className="text-sm text-gray-700 mb-2">{risk.description}</p>
                          
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                            <div>
                              <span className="font-medium text-gray-600">Probability:</span>
                              <span className={`ml-1 px-2 py-1 rounded text-xs ${
                                risk.probability === 'high' ? 'bg-red-100 text-red-800' :
                                risk.probability === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                                'bg-green-100 text-green-800'
                              }`}>
                                {risk.probability.toUpperCase()}
                              </span>
                            </div>
                            <div>
                              <span className="font-medium text-gray-600">Impact:</span>
                              <span className={`ml-1 px-2 py-1 rounded text-xs ${
                                risk.impact === 'high' ? 'bg-red-100 text-red-800' :
                                risk.impact === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                                'bg-green-100 text-green-800'
                              }`}>
                                {risk.impact.toUpperCase()}
                              </span>
                            </div>
                            <div>
                              <span className="font-medium text-gray-600">Score:</span>
                              <span className="ml-1 font-semibold">{riskScore}</span>
                            </div>
                            <div>
                              <span className="font-medium text-gray-600">Owner:</span>
                              <span className="ml-1">{risk.owner}</span>
                            </div>
                          </div>
                          
                          {risk.mitigation && (
                            <div className="mt-3 p-3 bg-white rounded border">
                              <p className="text-sm font-medium text-gray-600 mb-1">Mitigation Strategy:</p>
                              <p className="text-sm text-gray-700">{risk.mitigation}</p>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {activeTab === 'issues' && (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-medium text-gray-900">Issue Tracker</h3>
                <button
                  onClick={() => setShowAddIssue(true)}
                  className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
                  data-testid="add-issue-button"
                >
                  <PlusIcon className="h-4 w-4 mr-2" />
                  Add Issue
                </button>
              </div>

              <div className="space-y-3">
                {mockIssues.map((issue) => (
                  <div key={issue.id} className="border rounded-lg p-4 bg-white">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h4 className="font-medium text-gray-900">{issue.title}</h4>
                          <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(issue.status)}`}>
                            {issue.status.replace('_', ' ').toUpperCase()}
                          </span>
                          <span className={`px-2 py-1 rounded text-xs font-medium ${getPriorityColor(issue.priority)}`}>
                            {issue.priority.toUpperCase()}
                          </span>
                        </div>
                        
                        <p className="text-sm text-gray-700 mb-3">{issue.description}</p>
                        
                        <div className="flex items-center space-x-4 text-sm text-gray-600">
                          <div className="flex items-center">
                            <UserIcon className="h-4 w-4 mr-1" />
                            {issue.assignee}
                          </div>
                          <div className="flex items-center">
                            <ClockIcon className="h-4 w-4 mr-1" />
                            Created: {new Date(issue.createdAt).toLocaleDateString()}
                          </div>
                          {issue.resolvedAt && (
                            <div className="flex items-center">
                              <ClockIcon className="h-4 w-4 mr-1" />
                              Resolved: {new Date(issue.resolvedAt).toLocaleDateString()}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'decisions' && (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-medium text-gray-900">Decision Log</h3>
                <button className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700">
                  <PlusIcon className="h-4 w-4 mr-2" />
                  Add Decision
                </button>
              </div>

              <div className="space-y-3">
                {[
                  {
                    id: '1',
                    title: 'Technology Stack Selection',
                    description: 'Decided to use React with TypeScript for frontend development',
                    decisionMaker: 'Tech Lead',
                    date: '2024-01-10',
                    status: 'approved'
                  },
                  {
                    id: '2',
                    title: 'Database Migration Strategy',
                    description: 'Implement phased migration approach to minimize downtime',
                    decisionMaker: 'Project Manager',
                    date: '2024-01-15',
                    status: 'approved'
                  },
                  {
                    id: '3',
                    title: 'Third-party Integration Approach',
                    description: 'Use REST APIs instead of direct database connections',
                    decisionMaker: 'Architecture Team',
                    date: '2024-01-20',
                    status: 'pending'
                  }
                ].map((decision) => (
                  <div key={decision.id} className="border rounded-lg p-4 bg-white">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h4 className="font-medium text-gray-900">{decision.title}</h4>
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            decision.status === 'approved' ? 'bg-green-100 text-green-800' :
                            decision.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-gray-100 text-gray-800'
                          }`}>
                            {decision.status.toUpperCase()}
                          </span>
                        </div>
                        
                        <p className="text-sm text-gray-700 mb-3">{decision.description}</p>
                        
                        <div className="flex items-center space-x-4 text-sm text-gray-600">
                          <div>Decision Maker: {decision.decisionMaker}</div>
                          <div>Date: {new Date(decision.date).toLocaleDateString()}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};