export interface Loan {
  id: number;
  company: number;
  loan_officer: number;
  loan_officer_name: string;
  applicant_name: string;
  amount: number;
  interest_rate: number;
  term_months: number;
  status: 'PENDING' | 'APPROVED' | 'REJECTED' | 'COMPLETED';
  created_at: string;
  updated_at: string;
  repayment_progress: number;
}

export interface LoanFormData {
  applicant_name: string;
  amount: number;
  interest_rate: number;
  term_months: number;
}

export interface LoanRepayment {
  id: number;
  loan: number;
  amount: number;
  due_date: string;
  paid_date: string | null;
  is_paid: boolean;
} 