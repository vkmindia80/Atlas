export enum ProjectType {
  SOFTWARE_DEVELOPMENT = 'software_development',
  INFRASTRUCTURE = 'infrastructure',
  RESEARCH = 'research',
  MARKETING = 'marketing',
  PROCESS_IMPROVEMENT = 'process_improvement',
  COMPLIANCE = 'compliance',
  OTHER = 'other'
}

export enum ProjectMethodology {
  WATERFALL = 'waterfall',
  AGILE = 'agile',
  SCRUM = 'scrum',
  KANBAN = 'kanban',
  HYBRID = 'hybrid',
  LEAN = 'lean'
}

export interface ProjectFinancials {
  total_budget: number;
  allocated_budget: number;
  spent_amount: number;
  committed_amount: number;
  forecasted_cost: number;
  budget_variance: number;
  cost_to_complete: number;
  labor_cost: number;
  material_cost: number;
  vendor_cost: number;
  overhead_cost: number;
}

export interface Project {
  id: string;
  name: string;
  code: string;
  description?: string;
  project_type: ProjectType;
  methodology: ProjectMethodology;
  status: import('./portfolio').Status;
  health_status: import('./portfolio').HealthStatus;
  priority: import('./portfolio').Priority;
  portfolio_id?: string;
  project_manager_id: string;
  sponsor_id?: string;
  planned_start_date?: string;
  planned_end_date?: string;
  actual_start_date?: string;
  actual_end_date?: string;
  percent_complete: number;
  financials: ProjectFinancials;
  risk_score: number;
  open_issues_count: number;
  open_risks_count: number;
  team_size: number;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  name: string;
  code: string;
  description?: string;
  project_type: ProjectType;
  methodology: ProjectMethodology;
  priority: import('./portfolio').Priority;
  portfolio_id?: string;
  parent_project_id?: string;
  project_manager_id: string;
  sponsor_id?: string;
  planned_start_date?: string;
  planned_end_date?: string;
}

export interface ProjectUpdate {
  name?: string;
  description?: string;
  project_type?: ProjectType;
  methodology?: ProjectMethodology;
  status?: import('./portfolio').Status;
  health_status?: import('./portfolio').HealthStatus;
  priority?: import('./portfolio').Priority;
  portfolio_id?: string;
  project_manager_id?: string;
  sponsor_id?: string;
  planned_start_date?: string;
  planned_end_date?: string;
  actual_start_date?: string;
  actual_end_date?: string;
  percent_complete?: number;
  team_members?: string[];
}