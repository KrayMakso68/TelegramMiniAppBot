export interface Subscription {
  email_name: string;
  url: string;
  user_id: number;
  server_id: number;
  end_date: Date | null;
  is_active: boolean;
}
