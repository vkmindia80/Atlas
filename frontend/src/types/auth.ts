export enum UserRole {
  ADMIN = 'admin',
  PMO_ADMIN = 'pmo_admin',
  PORTFOLIO_MANAGER = 'portfolio_manager',
  PROJECT_MANAGER = 'project_manager',
  RESOURCE = 'resource',
  FINANCE = 'finance',
  VIEWER = 'viewer'
}

export enum UserStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  SUSPENDED = 'suspended',
  PENDING_VERIFICATION = 'pending_verification'
}

export interface User {
  id: string;
  username: string;
  email: string;
  full_name: string;
  role: UserRole;
  status: UserStatus;
  job_title?: string;
  department?: string;
  phone?: string;
  avatar_url?: string;
  last_login?: string;
  created_at: string;
  updated_at: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
  tenant_code: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  loading: boolean;
  error: string | null;
}

export interface TenantRegistration {
  name: string;
  code: string;
  domain: string;
  admin_email: string;
  admin_name: string;
  phone?: string;
  plan: 'starter' | 'professional' | 'enterprise';
}