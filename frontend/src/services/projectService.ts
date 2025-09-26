import axios from 'axios';
import { Project, ProjectCreate, ProjectDetail, ProjectTask, ProjectIssue, ProjectRisk, ProjectIntakeForm } from '../types/project';

const API_BASE = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

class ProjectService {
  private getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    };
  }

  async getProjects(params?: {
    skip?: number;
    limit?: number;
    status?: string;
    portfolio_id?: string;
    project_manager_id?: string;
    project_type?: string;
  }): Promise<Project[]> {
    const response = await axios.get(`${API_BASE}/api/v1/projects/`, {
      ...this.getAuthHeaders(),
      params,
    });
    return response.data;
  }

  async getProject(id: string): Promise<Project> {
    const response = await axios.get(`${API_BASE}/api/v1/projects/${id}`, this.getAuthHeaders());
    return response.data;
  }

  async getProjectDetail(id: string): Promise<ProjectDetail> {
    const response = await axios.get(`${API_BASE}/api/v1/projects/${id}`, this.getAuthHeaders());
    return response.data;
  }

  async createProject(project: ProjectCreate): Promise<Project> {
    const response = await axios.post(`${API_BASE}/api/v1/projects/`, project, this.getAuthHeaders());
    return response.data;
  }

  async updateProject(id: string, project: Partial<Project>): Promise<Project> {
    const response = await axios.put(`${API_BASE}/api/v1/projects/${id}`, project, this.getAuthHeaders());
    return response.data;
  }

  async deleteProject(id: string): Promise<void> {
    await axios.delete(`${API_BASE}/api/v1/projects/${id}`, this.getAuthHeaders());
  }

  // Task management
  async createTask(projectId: string, task: Partial<ProjectTask>): Promise<void> {
    await axios.post(`${API_BASE}/api/v1/projects/${projectId}/tasks`, task, this.getAuthHeaders());
  }

  async updateTask(projectId: string, taskId: string, task: Partial<ProjectTask>): Promise<void> {
    await axios.put(`${API_BASE}/api/v1/projects/${projectId}/tasks/${taskId}`, task, this.getAuthHeaders());
  }

  async deleteTask(projectId: string, taskId: string): Promise<void> {
    await axios.delete(`${API_BASE}/api/v1/projects/${projectId}/tasks/${taskId}`, this.getAuthHeaders());
  }

  // Issue management
  async createIssue(projectId: string, issue: Partial<ProjectIssue>): Promise<void> {
    await axios.post(`${API_BASE}/api/v1/projects/${projectId}/issues`, issue, this.getAuthHeaders());
  }

  // Risk management
  async createRisk(projectId: string, risk: Partial<ProjectRisk>): Promise<void> {
    await axios.post(`${API_BASE}/api/v1/projects/${projectId}/risks`, risk, this.getAuthHeaders());
  }

  // Baseline management
  async createBaseline(projectId: string, baselineData: any): Promise<void> {
    await axios.post(`${API_BASE}/api/v1/projects/${projectId}/baselines`, baselineData, this.getAuthHeaders());
  }

  // Approval workflow
  async requestApproval(projectId: string, approvalData: any): Promise<void> {
    await axios.post(`${API_BASE}/api/v1/projects/${projectId}/approvals`, approvalData, this.getAuthHeaders());
  }

  async processApproval(projectId: string, approvalId: string, decision: any): Promise<void> {
    await axios.put(
      `${API_BASE}/api/v1/projects/${projectId}/approvals/${approvalId}`,
      decision,
      this.getAuthHeaders()
    );
  }

  // Bulk operations
  async bulkUpdateStatus(updates: Array<{ project_id: string; status: string }>): Promise<any> {
    const response = await axios.post(
      `${API_BASE}/api/v1/projects/bulk-update-status`,
      updates,
      this.getAuthHeaders()
    );
    return response.data;
  }

  async importFromCSV(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(
      `${API_BASE}/api/v1/projects/import-csv`,
      formData,
      {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  }

  // Project templates
  async getProjectTemplates(): Promise<any[]> {
    const response = await axios.get(`${API_BASE}/api/v1/projects/templates/`, this.getAuthHeaders());
    return response.data;
  }

  async createProjectTemplate(template: any): Promise<void> {
    await axios.post(`${API_BASE}/api/v1/projects/templates/`, template, this.getAuthHeaders());
  }

  // Intake form
  async createProjectFromIntake(intakeData: {
    intake_data: ProjectIntakeForm;
    template_id?: string;
    auto_approve?: boolean;
  }): Promise<any> {
    const response = await axios.post(
      `${API_BASE}/api/v1/projects/from-intake`,
      intakeData,
      this.getAuthHeaders()
    );
    return response.data;
  }
}

export const projectService = new ProjectService();