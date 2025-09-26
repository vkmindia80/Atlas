import React, { useState } from 'react';
import { 
  DocumentIcon, 
  FolderIcon,
  CloudArrowUpIcon,
  MagnifyingGlassIcon,
  EllipsisHorizontalIcon,
  CalendarIcon,
  UserIcon,
  ArrowDownTrayIcon
} from '@heroicons/react/24/outline';
import { ProjectDetail } from '../../types/project';

interface ProjectDocumentsProps {
  projectDetail: ProjectDetail;
  onUpdate: () => void;
}

interface Document {
  id: string;
  name: string;
  type: 'document' | 'spreadsheet' | 'presentation' | 'image' | 'other';
  size: number;
  category: string;
  uploadedBy: string;
  uploadedAt: string;
  version: string;
  description?: string;
  tags: string[];
}

interface Folder {
  id: string;
  name: string;
  documents: Document[];
  createdAt: string;
}

export const ProjectDocuments: React.FC<ProjectDocumentsProps> = ({
  projectDetail,
  onUpdate
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [viewMode, setViewMode] = useState<'list' | 'grid'>('list');

  // Mock data for demonstration
  const mockFolders: Folder[] = [
    {
      id: '1',
      name: 'Requirements',
      createdAt: '2024-01-10',
      documents: [
        {
          id: '1',
          name: 'Business Requirements Document.docx',
          type: 'document',
          size: 2048000,
          category: 'requirements',
          uploadedBy: 'Alice Johnson',
          uploadedAt: '2024-01-15',
          version: '2.1',
          description: 'Comprehensive business requirements for the project',
          tags: ['requirements', 'business', 'stakeholders']
        },
        {
          id: '2',
          name: 'Technical Specifications.pdf',
          type: 'document',
          size: 1536000,
          category: 'requirements',
          uploadedBy: 'Bob Smith',
          uploadedAt: '2024-01-18',
          version: '1.3',
          tags: ['technical', 'specifications', 'architecture']
        }
      ]
    },
    {
      id: '2',
      name: 'Design',
      createdAt: '2024-01-12',
      documents: [
        {
          id: '3',
          name: 'UI Mockups.figma',
          type: 'other',
          size: 5242880,
          category: 'design',
          uploadedBy: 'Carol Davis',
          uploadedAt: '2024-01-20',
          version: '3.0',
          description: 'User interface mockups and prototypes',
          tags: ['ui', 'mockups', 'design', 'figma']
        },
        {
          id: '4',
          name: 'System Architecture.png',
          type: 'image',
          size: 1024000,
          category: 'design',
          uploadedBy: 'David Wilson',
          uploadedAt: '2024-01-22',
          version: '1.0',
          tags: ['architecture', 'diagram', 'system']
        }
      ]
    },
    {
      id: '3',
      name: 'Reports',
      createdAt: '2024-01-14',
      documents: [
        {
          id: '5',
          name: 'Project Status Report.xlsx',
          type: 'spreadsheet',
          size: 512000,
          category: 'reports',
          uploadedBy: 'Emma Brown',
          uploadedAt: '2024-01-25',
          version: '1.2',
          description: 'Weekly project status and metrics',
          tags: ['status', 'metrics', 'weekly']
        },
        {
          id: '6',
          name: 'Risk Assessment.pptx',
          type: 'presentation',
          size: 3072000,
          category: 'reports',
          uploadedBy: 'Frank Miller',
          uploadedAt: '2024-01-23',
          version: '1.1',
          tags: ['risk', 'assessment', 'presentation']
        }
      ]
    }
  ];

  const allDocuments = mockFolders.flatMap(folder => folder.documents);

  const filteredDocuments = allDocuments.filter(doc => {
    const matchesSearch = doc.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         doc.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCategory = selectedCategory === 'all' || doc.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'document':
        return '📄';
      case 'spreadsheet':
        return '📊';
      case 'presentation':
        return '📽️';
      case 'image':
        return '🖼️';
      default:
        return '📎';
    }
  };

  const categories = ['all', ...Array.from(new Set(allDocuments.map(doc => doc.category)))];

  return (
    <div className="space-y-6" data-testid="project-documents">
      {/* Header with Upload */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">Project Documents</h2>
            <p className="text-sm text-gray-600 mt-1">
              Manage and organize all project-related documents and files
            </p>
          </div>
          
          <div className="flex space-x-3">
            <button className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
              <FolderIcon className="h-4 w-4 mr-2" />
              New Folder
            </button>
            <button 
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
              data-testid="upload-document-button"
            >
              <CloudArrowUpIcon className="h-4 w-4 mr-2" />
              Upload Document
            </button>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500"
                placeholder="Search documents..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                data-testid="document-search"
              />
            </div>
          </div>
          
          <div className="flex space-x-3">
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="block pl-3 pr-10 py-2 text-base border border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 rounded-md"
              data-testid="category-filter"
            >
              {categories.map(category => (
                <option key={category} value={category}>
                  {category === 'all' ? 'All Categories' : category.charAt(0).toUpperCase() + category.slice(1)}
                </option>
              ))}
            </select>
            
            <div className="flex rounded-md shadow-sm">
              <button
                onClick={() => setViewMode('list')}
                className={`px-3 py-2 text-sm font-medium rounded-l-md border ${
                  viewMode === 'list'
                    ? 'bg-primary-600 text-white border-primary-600'
                    : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                }`}
              >
                List
              </button>
              <button
                onClick={() => setViewMode('grid')}
                className={`px-3 py-2 text-sm font-medium rounded-r-md border-t border-r border-b ${
                  viewMode === 'grid'
                    ? 'bg-primary-600 text-white border-primary-600'
                    : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                }`}
              >
                Grid
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Document Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-lg shadow text-center">
          <div className="text-2xl font-bold text-gray-900">{allDocuments.length}</div>
          <div className="text-sm text-gray-600">Total Documents</div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow text-center">
          <div className="text-2xl font-bold text-gray-900">{mockFolders.length}</div>
          <div className="text-sm text-gray-600">Folders</div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow text-center">
          <div className="text-2xl font-bold text-gray-900">
            {formatFileSize(allDocuments.reduce((sum, doc) => sum + doc.size, 0))}
          </div>
          <div className="text-sm text-gray-600">Total Size</div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow text-center">
          <div className="text-2xl font-bold text-gray-900">
            {new Set(allDocuments.map(doc => doc.uploadedBy)).size}
          </div>
          <div className="text-sm text-gray-600">Contributors</div>
        </div>
      </div>

      {/* Documents List/Grid */}
      <div className="bg-white rounded-lg shadow">
        {viewMode === 'list' ? (
          <div className="divide-y divide-gray-200">
            <div className="px-6 py-3 bg-gray-50">
              <div className="flex items-center space-x-4 text-sm font-medium text-gray-500">
                <div className="flex-1">Name</div>
                <div className="w-24">Size</div>
                <div className="w-32">Modified</div>
                <div className="w-32">Modified By</div>
                <div className="w-20">Version</div>
                <div className="w-8"></div>
              </div>
            </div>
            
            {filteredDocuments.map((doc) => (
              <div key={doc.id} className="px-6 py-4 hover:bg-gray-50">
                <div className="flex items-center space-x-4">
                  <div className="flex-1 flex items-center space-x-3">
                    <span className="text-2xl">{getFileIcon(doc.type)}</span>
                    <div>
                      <p className="text-sm font-medium text-gray-900">{doc.name}</p>
                      {doc.description && (
                        <p className="text-xs text-gray-500">{doc.description}</p>
                      )}
                      <div className="flex flex-wrap gap-1 mt-1">
                        {doc.tags.slice(0, 3).map(tag => (
                          <span key={tag} className="inline-block bg-gray-100 text-gray-600 text-xs px-2 py-1 rounded">
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                  <div className="w-24 text-sm text-gray-500">
                    {formatFileSize(doc.size)}
                  </div>
                  <div className="w-32 text-sm text-gray-500">
                    {new Date(doc.uploadedAt).toLocaleDateString()}
                  </div>
                  <div className="w-32 text-sm text-gray-500">
                    {doc.uploadedBy}
                  </div>
                  <div className="w-20 text-sm text-gray-500">
                    v{doc.version}
                  </div>
                  <div className="w-8">
                    <button className="text-gray-400 hover:text-gray-600">
                      <EllipsisHorizontalIcon className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {filteredDocuments.map((doc) => (
                <div key={doc.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="text-center mb-3">
                    <span className="text-4xl">{getFileIcon(doc.type)}</span>
                  </div>
                  
                  <h4 className="font-medium text-gray-900 text-sm mb-2 line-clamp-2">{doc.name}</h4>
                  
                  <div className="space-y-2 text-xs text-gray-500">
                    <div className="flex items-center">
                      <UserIcon className="h-3 w-3 mr-1" />
                      {doc.uploadedBy}
                    </div>
                    <div className="flex items-center">
                      <CalendarIcon className="h-3 w-3 mr-1" />
                      {new Date(doc.uploadedAt).toLocaleDateString()}
                    </div>
                    <div>{formatFileSize(doc.size)} • v{doc.version}</div>
                  </div>
                  
                  <div className="flex flex-wrap gap-1 mt-3">
                    {doc.tags.slice(0, 2).map(tag => (
                      <span key={tag} className="inline-block bg-gray-100 text-gray-600 text-xs px-2 py-1 rounded">
                        {tag}
                      </span>
                    ))}
                  </div>
                  
                  <div className="flex justify-between items-center mt-4">
                    <button className="text-primary-600 hover:text-primary-800 text-sm font-medium">
                      View
                    </button>
                    <button className="text-gray-400 hover:text-gray-600">
                      <ArrowDownTrayIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {filteredDocuments.length === 0 && (
          <div className="text-center py-12">
            <DocumentIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No documents found</h3>
            <p className="text-gray-600">
              {searchTerm ? 'Try adjusting your search criteria' : 'Upload your first document to get started'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};