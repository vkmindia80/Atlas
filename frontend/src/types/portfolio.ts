export enum PortfolioType {
  STRATEGIC = 'strategic',
  OPERATIONAL = 'operational',
  INNOVATION = 'innovation',
  MAINTENANCE = 'maintenance'
}

export enum Priority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export enum Status {
  DRAFT = 'draft',
  ACTIVE = 'active',
  ON_HOLD = 'on_hold',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled'
}

export enum HealthStatus {
  GREEN = 'green',
  YELLOW = 'yellow',
  RED = 'red'
}

export interface FinancialMetrics {
  total_budget: number;
  allocated_budget: number;
  spent_amount: number;
  committed_amount: number;
  forecasted_cost: number;
  npv?: number;
  irr?: number;
  roi_percentage?: number;
  payback_period_months?: number;
}

export interface RiskMetrics {
  risk_score: number;
  high_risks_count: number;
  medium_risks_count: number;
  low_risks_count: number;
  overdue_risks_count: number;
}

export interface Portfolio {
  id: string;
  name: string;
  code: string;
  description?: string;
  portfolio_type: PortfolioType;
  status: Status;
  health_status: HealthStatus;
  priority: Priority;
  portfolio_manager_id: string;
  sponsors: string[];
  stakeholders: string[];
  start_date?: string;
  end_date?: string;
  financial_metrics: FinancialMetrics;
  risk_metrics: RiskMetrics;
  project_count: number;
  created_at: string;
  updated_at: string;
}

export interface PortfolioCreate {
  name: string;
  code: string;
  description?: string;
  portfolio_type: PortfolioType;
  priority: Priority;
  portfolio_manager_id: string;
  sponsors: string[];
  stakeholders: string[];
  start_date?: string;
  end_date?: string;
  business_case_url?: string;
}

export interface PortfolioUpdate {
  name?: string;
  description?: string;
  portfolio_type?: PortfolioType;
  status?: Status;
  health_status?: HealthStatus;
  priority?: Priority;
  portfolio_manager_id?: string;
  sponsors?: string[];
  stakeholders?: string[];
  start_date?: string;
  end_date?: string;
  business_case_url?: string;
}