// Export type aliases for better reusability
export type PortfolioType = 'strategic' | 'operational' | 'innovation' | 'maintenance';
export type Status = 'draft' | 'active' | 'on_hold' | 'completed' | 'cancelled';
export type HealthStatus = 'green' | 'yellow' | 'red';
export type Priority = 'low' | 'medium' | 'high' | 'critical';

export interface Portfolio {
  id: string;
  name: string;
  code: string;
  description?: string;
  portfolio_type: 'strategic' | 'operational' | 'innovation' | 'maintenance';
  status: 'draft' | 'active' | 'on_hold' | 'completed' | 'cancelled';
  health_status: 'green' | 'yellow' | 'red';
  priority: 'low' | 'medium' | 'high' | 'critical';
  portfolio_manager_id: string;
  sponsors: string[];
  stakeholders: string[];
  start_date?: string;
  end_date?: string;
  financial_metrics: {
    total_budget: number;
    allocated_budget: number;
    spent_amount: number;
    committed_amount: number;
    forecasted_cost: number;
    npv?: number;
    irr?: number;
    roi_percentage?: number;
    payback_period_months?: number;
  };
  risk_metrics: {
    risk_score: number;
    high_risks_count: number;
    medium_risks_count: number;
    low_risks_count: number;
    overdue_risks_count: number;
  };
  kpis: PortfolioKPI[];
  project_count: number;
  active_project_count: number;
  budget_utilization_percentage: number;
  created_at: string;
  updated_at: string;
}

export interface PortfolioKPI {
  id: string;
  name: string;
  description?: string;
  kpi_type: string;
  unit: string;
  target_value: number;
  current_value: number;
  baseline_value?: number;
  red_threshold?: number;
  yellow_threshold?: number;
  green_threshold?: number;
  calculation_method?: string;
  update_frequency: string;
  last_updated?: string;
}

export interface PortfolioProject {
  id: string;
  portfolio_id: string;
  project_id: string;
  project_name: string;
  project_status: string;
  strategic_weight: number;
  budget_allocation?: number;
  priority_ranking?: number;
  alignment_scores: Record<string, number>;
  added_date: string;
}

export interface PortfolioDashboard {
  portfolio: Portfolio;
  kpis: {
    status_counts: Record<string, number>;
    budget_summary: {
      total_budget: number;
      total_spent: number;
      total_committed: number;
    };
    risk_heatmap: Record<string, { count: number; avg_risk: number }>;
    total_projects: number;
    budget_utilization_percentage: number;
  };
}

export interface PortfolioCreate {
  name: string;
  code: string;
  description?: string;
  portfolio_type: 'strategic' | 'operational' | 'innovation' | 'maintenance';
  priority: 'low' | 'medium' | 'high' | 'critical';
  portfolio_manager_id: string;
  sponsors: string[];
  stakeholders: string[];
  start_date?: string;
  end_date?: string;
  business_case_url?: string;
}

export interface StrategicObjective {
  id: string;
  name: string;
  code: string;
  description?: string;
  objective_type: 'financial' | 'customer' | 'internal_process' | 'learning_growth' | 'strategic_initiative';
  status: 'draft' | 'active' | 'on_hold' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'critical';
  owner_id: string;
  stakeholders: string[];
  start_date?: string;
  target_date?: string;
  kpis: KPI[];
  parent_objective_id?: string;
  child_objective_ids: string[];
  created_at: string;
  updated_at: string;
}

export interface KPI {
  id: string;
  name: string;
  description?: string;
  measurement_unit: 'percentage' | 'currency' | 'count' | 'days' | 'score' | 'ratio';
  target_value: number;
  current_value: number;
  baseline_value?: number;
  threshold_red?: number;
  threshold_yellow?: number;
  threshold_green?: number;
  is_higher_better: boolean;
}