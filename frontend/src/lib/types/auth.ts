export interface LoginCredentials {
  username: string;
  password: string;
}

export type RegisterData = {
  username: string;
  password: string;
  email: string;
  company_name: string;
  registration_number: string;
  is_company_admin?: boolean;
};

export interface AuthResponse {
  access: string;
  refresh: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  is_company_admin: boolean;
  company?: number;
} 