export interface Project {
  id: string;
  name: string;
  code: string;
  description?: string;
  project_type: 'software_development' | 'infrastructure' | 'research' | 'marketing' | 'process_improvement' | 'compliance' | 'other';
  methodology: 'waterfall' | 'agile' | 'scrum' | 'kanban' | 'hybrid' | 'lean';
  status: 'draft' | 'active' | 'on_hold' | 'completed' | 'cancelled';
  health_status: 'green' | 'yellow' | 'red';
  priority: 'low' | 'medium' | 'high' | 'critical';
  current_phase?: 'initiation' | 'planning' | 'execution' | 'monitoring' | 'closure';
  portfolio_id?: string;
  parent_project_id?: string;
  template_id?: string;
  project_manager_id: string;
  sponsor_id?: string;
  team_members: string[];
  planned_start_date?: string;
  planned_end_date?: string;
  actual_start_date?: string;
  actual_end_date?: string;
  percent_complete: number;
  financials: ProjectFinancials;
  risk_score: number;
  team_size: number;
  created_at: string;
  updated_at: string;
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

export interface ProjectTask {
  id: string;
  name: string;
  description?: string;
  status: 'not_started' | 'in_progress' | 'on_hold' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'critical';
  assignee_id?: string;
  reviewer_id?: string;
  planned_start_date?: string;
  planned_end_date?: string;
  actual_start_date?: string;
  actual_end_date?: string;
  estimated_hours?: number;
  actual_hours?: number;
  percent_complete: number;
  parent_task_id?: string;
  subtasks: string[];
  dependencies: ProjectDependency[];
  labels: string[];
  tags: string[];
  story_points?: number;
}

export interface ProjectDependency {
  id: string;
  predecessor_project_id?: string;
  predecessor_task_id?: string;
  successor_project_id?: string;
  successor_task_id?: string;
  dependency_type: 'finish_to_start' | 'start_to_start' | 'finish_to_finish' | 'start_to_finish';
  lag_days: number;
  description?: string;
  is_critical_path: boolean;
}

export interface ProjectIssue {
  id: string;
  title: string;
  description?: string;
  issue_type: 'bug' | 'task' | 'story' | 'epic' | 'improvement' | 'blocker';
  status: 'draft' | 'active' | 'on_hold' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'critical';
  reporter_id: string;
  assignee_id?: string;
  created_date: string;
  due_date?: string;
  resolved_date?: string;
  related_task_id?: string;
  blocked_tasks: string[];
  resolution?: string;
  resolution_notes?: string;
  labels: string[];
  estimated_hours?: number;
}

export interface ProjectRisk {
  id: string;
  title: string;
  description: string;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  probability: number;
  impact: number;
  owner_id: string;
  identified_by: string;
  identified_date: string;
  status: 'draft' | 'active' | 'on_hold' | 'completed' | 'cancelled';
  mitigation_plan?: string;
  contingency_plan?: string;
  mitigation_cost?: number;
  target_resolution_date?: string;
  actual_resolution_date?: string;
  affected_tasks: string[];
  affected_milestones: string[];
}

export interface Milestone {
  id: string;
  name: string;
  description?: string;
  planned_date: string;
  actual_date?: string;
  status: 'planned' | 'in_progress' | 'completed' | 'delayed' | 'cancelled';
  deliverables: string[];
  dependencies: string[];
}

export interface ProjectDetail {
  project: Project;
  tasks: ProjectTask[];
  milestones: Milestone[];
  risks: ProjectRisk[];
  issues: ProjectIssue[];
  dependencies: ProjectDependency[];
  approvals: ProjectApproval[];
  baselines: ProjectBaseline[];
  task_summary: {
    total: number;
    not_started: number;
    in_progress: number;
    completed: number;
    on_hold: number;
  };
}

export interface ProjectApproval {
  id: string;
  approval_type: string;
  status: 'pending' | 'approved' | 'rejected' | 'withdrawn';
  requested_by: string;
  request_date: string;
  description: string;
  justification?: string;
  approver_id: string;
  approval_date?: string;
  approval_comments?: string;
  document_urls: string[];
}

export interface ProjectBaseline {
  id: string;
  name: string;
  description?: string;
  baseline_date: string;
  created_by: string;
  planned_start_date?: string;
  planned_end_date?: string;
  total_budget: number;
  milestones_snapshot: Milestone[];
  tasks_snapshot: ProjectTask[];
  schedule_variance_days?: number;
  cost_variance?: number;
  scope_change_count: number;
}

export interface ProjectCreate {
  name: string;
  code: string;
  description?: string;
  project_type: string;
  methodology?: string;
  priority?: string;
  portfolio_id?: string;
  parent_project_id?: string;
  project_manager_id: string;
  sponsor_id?: string;
  planned_start_date?: string;
  planned_end_date?: string;
}

export interface ProjectIntakeForm {
  project_name: string;
  business_justification: string;
  project_type: string;
  methodology?: string;
  priority?: string;
  requested_start_date?: string;
  target_end_date?: string;
  estimated_budget?: number;
  budget_source?: string;
  project_sponsor: string;
  business_owner: string;
  preferred_project_manager?: string;
  portfolio_id?: string;
  strategic_objectives: string[];
  project_scope: string;
  key_requirements: string[];
  success_criteria: string[];
  estimated_team_size?: number;
  required_skills: string[];
  identified_risks: string[];
  risk_mitigation_notes?: string;
  business_case_url?: string;
  supporting_documents: string[];
}