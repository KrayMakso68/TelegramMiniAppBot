export interface Subscription {
  emailName: string;
  url: string;
  userId: number;
  serverId: number;
  endDate: Date | null;
  isActive: boolean;
}
