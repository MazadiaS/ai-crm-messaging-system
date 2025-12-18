// User types
export enum UserRole {
  ADMIN = 'admin',
  MANAGER = 'manager',
  VIEWER = 'viewer',
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  created_at: string;
  updated_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

// Contact types
export enum ContactSegment {
  VIP = 'VIP',
  REGULAR = 'regular',
  NEW_CLIENT = 'new_client',
  PARTNER = 'partner',
}

export enum Language {
  RU = 'ru',
  EN = 'en',
  UZ = 'uz',
}

export interface Contact {
  id: string;
  name: string;
  email: string;
  phone: string | null;
  segment: ContactSegment;
  birthday: string | null;
  company: string | null;
  position: string | null;
  language: Language;
  tags: string[];
  custom_fields: Record<string, any>;
  last_interaction_date: string | null;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface ContactCreate {
  name: string;
  email: string;
  phone?: string;
  segment?: ContactSegment;
  birthday?: string;
  company?: string;
  position?: string;
  language?: Language;
  tags?: string[];
  custom_fields?: Record<string, any>;
}

// Message types
export enum OccasionType {
  BIRTHDAY = 'birthday',
  NEW_YEAR = 'new_year',
  HOLIDAY = 'holiday',
  PROMOTION = 'promotion',
  CUSTOM = 'custom',
}

export enum MessageStatus {
  DRAFT = 'draft',
  PENDING_APPROVAL = 'pending_approval',
  APPROVED = 'approved',
  SENT = 'sent',
  FAILED = 'failed',
  REJECTED = 'rejected',
}

export enum GeneratedBy {
  AI = 'AI',
  MANUAL = 'manual',
}

export interface Message {
  id: string;
  contact_id: string;
  occasion_type: OccasionType;
  content: string;
  status: MessageStatus;
  generated_by: GeneratedBy;
  created_by: string;
  approved_by: string | null;
  sent_at: string | null;
  approved_at: string | null;
  scheduled_for: string | null;
  metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface MessageGenerate {
  contact_id: string;
  occasion_type: OccasionType;
  custom_context?: string;
  tone?: string;
}

// Campaign types
export enum ScheduleType {
  IMMEDIATE = 'immediate',
  SCHEDULED = 'scheduled',
  RECURRING = 'recurring',
}

export enum CampaignStatus {
  DRAFT = 'draft',
  ACTIVE = 'active',
  PAUSED = 'paused',
  COMPLETED = 'completed',
}

export interface Campaign {
  id: string;
  name: string;
  description: string | null;
  occasion_type: OccasionType;
  segment_filter: Record<string, any>;
  schedule_type: ScheduleType;
  scheduled_at: string | null;
  recurrence_rule: string | null;
  status: CampaignStatus;
  created_by: string;
  stats: Record<string, any>;
  created_at: string;
  updated_at: string;
}

// Analytics types
export interface DashboardStats {
  total_contacts: number;
  total_messages: number;
  pending_approval: number;
  approved: number;
  sent: number;
  active_campaigns: number;
  messages_this_month: number;
  generated_at: string;
}

// Pagination
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}
