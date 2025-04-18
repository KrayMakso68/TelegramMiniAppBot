export interface Subscription {
  id: number;
  name: string;
  email: string;
  url: string;
  userId: number;
  serverId: number;
  endDate: Date | null;
  isActive: boolean;
}
