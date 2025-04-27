export interface ClientInfo {
  email: string;
  enable: true;
  id: number | string;
  inboundId: number | null;
  up: number;
  down: number;
  expiryTime: number;
  total: number;
  reset: number;
  flow: string;
  limitIp: number;
  subId: string;
  tgId: string;
  totalGB: number;
}

export interface Client {
  connectUrl: string;
  uuid: string;
  email: string;
  inboundName: string;
  remainingSeconds: number;
  active: boolean;
}

export interface ClientCreate {
  shortName: string;
  protocol: string;
  serverId: number;
  months: number;
  price: number;
}

export interface ClientUpdate {
  id: number;
  serverId: number;
  months: number;
  price: number;
}
