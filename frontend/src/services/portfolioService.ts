import axios from 'axios';
import { Portfolio, PortfolioCreate, PortfolioDashboard, PortfolioProject, StrategicObjective } from '../types/portfolio';

const API_BASE = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

class PortfolioService {
  private getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    };
  }

  async getPortfolios(params?: {
    skip?: number;
    limit?: number;
    status?: string;
    portfolio_type?: string;
    portfolio_manager_id?: string;
  }): Promise<Portfolio[]> {
    const response = await axios.get(`${API_BASE}/api/v1/portfolios/`, {
      ...this.getAuthHeaders(),
      params,
    });
    return response.data;
  }

  async getPortfolio(id: string): Promise<Portfolio> {
    const response = await axios.get(`${API_BASE}/api/v1/portfolios/${id}`, this.getAuthHeaders());
    return response.data;
  }

  async createPortfolio(portfolio: PortfolioCreate): Promise<Portfolio> {
    const response = await axios.post(`${API_BASE}/api/v1/portfolios/`, portfolio, this.getAuthHeaders());
    return response.data;
  }

  async updatePortfolio(id: string, portfolio: Partial<Portfolio>): Promise<Portfolio> {
    const response = await axios.put(`${API_BASE}/api/v1/portfolios/${id}`, portfolio, this.getAuthHeaders());
    return response.data;
  }

  async deletePortfolio(id: string): Promise<void> {
    await axios.delete(`${API_BASE}/api/v1/portfolios/${id}`, this.getAuthHeaders());
  }

  async getPortfolioProjects(portfolioId: string): Promise<PortfolioProject[]> {
    const response = await axios.get(
      `${API_BASE}/api/v1/portfolios/${portfolioId}/projects`,
      this.getAuthHeaders()
    );
    return response.data;
  }

  async addProjectToPortfolio(
    portfolioId: string,
    projectId: string,
    relationshipData?: any
  ): Promise<void> {
    await axios.post(
      `${API_BASE}/api/v1/portfolios/${portfolioId}/projects/${projectId}`,
      relationshipData || {},
      this.getAuthHeaders()
    );
  }

  async removeProjectFromPortfolio(portfolioId: string, projectId: string): Promise<void> {
    await axios.delete(
      `${API_BASE}/api/v1/portfolios/${portfolioId}/projects/${projectId}`,
      this.getAuthHeaders()
    );
  }

  async getPortfolioDashboard(portfolioId: string): Promise<PortfolioDashboard> {
    const response = await axios.get(
      `${API_BASE}/api/v1/portfolios/${portfolioId}/dashboard`,
      this.getAuthHeaders()
    );
    return response.data;
  }

  async createPortfolioSnapshot(portfolioId: string, snapshotData: any): Promise<void> {
    await axios.post(
      `${API_BASE}/api/v1/portfolios/${portfolioId}/snapshots`,
      snapshotData,
      this.getAuthHeaders()
    );
  }

  // Strategic Objectives
  async getStrategicObjectives(): Promise<StrategicObjective[]> {
    const response = await axios.get(`${API_BASE}/api/v1/portfolios/objectives/`, this.getAuthHeaders());
    return response.data;
  }

  async createStrategicObjective(objective: any): Promise<StrategicObjective> {
    const response = await axios.post(
      `${API_BASE}/api/v1/portfolios/objectives/`,
      objective,
      this.getAuthHeaders()
    );
    return response.data;
  }

  async updateStrategicObjective(id: string, objective: any): Promise<StrategicObjective> {
    const response = await axios.put(
      `${API_BASE}/api/v1/portfolios/objectives/${id}`,
      objective,
      this.getAuthHeaders()
    );
    return response.data;
  }
}

export const portfolioService = new PortfolioService();