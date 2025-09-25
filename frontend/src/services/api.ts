import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { AuthResponse, LoginCredentials, TenantRegistration } from '../types/auth';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for handling token refresh
    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          const refreshToken = localStorage.getItem('refresh_token');
          if (refreshToken) {
            try {
              const response = await this.refreshToken(refreshToken);
              localStorage.setItem('access_token', response.access_token);
              // Retry original request
              return this.api.request(error.config);
            } catch (refreshError) {
              this.clearTokens();
              window.location.href = '/login';
            }
          } else {
            this.clearTokens();
            window.location.href = '/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  private clearTokens(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  // Authentication methods
  async registerTenant(data: TenantRegistration): Promise<any> {
    const response = await this.api.post('/api/v1/auth/register-tenant', data);
    return response.data;
  }

  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await this.api.post('/api/v1/auth/login', credentials);
    const authData = response.data;
    
    // Store tokens
    localStorage.setItem('access_token', authData.access_token);
    localStorage.setItem('refresh_token', authData.refresh_token);
    
    return authData;
  }

  async refreshToken(refreshToken: string): Promise<{ access_token: string; token_type: string; expires_in: number }> {
    const response = await this.api.post('/api/v1/auth/refresh', { refresh_token: refreshToken });
    return response.data;
  }

  async logout(): Promise<void> {
    try {
      await this.api.post('/api/v1/auth/logout');
    } finally {
      this.clearTokens();
    }
  }

  async getCurrentUser(): Promise<any> {
    const response = await this.api.get('/api/v1/auth/me');
    return response.data;
  }

  // Generic CRUD methods
  async get<T>(endpoint: string, params?: any): Promise<T> {
    const response: AxiosResponse<T> = await this.api.get(endpoint, { params });
    return response.data;
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    const response: AxiosResponse<T> = await this.api.post(endpoint, data);
    return response.data;
  }

  async put<T>(endpoint: string, data: any): Promise<T> {
    const response: AxiosResponse<T> = await this.api.put(endpoint, data);
    return response.data;
  }

  async delete<T>(endpoint: string): Promise<T> {
    const response: AxiosResponse<T> = await this.api.delete(endpoint);
    return response.data;
  }

  // Health check
  async healthCheck(): Promise<any> {
    const response = await this.api.get('/health');
    return response.data;
  }
}

export const apiService = new ApiService();
export default apiService;