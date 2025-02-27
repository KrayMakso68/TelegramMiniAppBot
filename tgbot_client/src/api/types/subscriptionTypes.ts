export interface Subscription {
  id: number;
  emailName: string;
  url: string;
  userId: number;
  serverId: number;
  endDate: Date | null;
  isActive: boolean;
}
