export interface ConnectInfo {
  email: string,
  enable: true,
  id: number | string,
  inboundId: number | null,
  up: number,
  down: number,
  expiryTime: number,
  total: number,
  reset: number,
  flow: string,
  limitIp: number,
  subId: string,
  tgId: string,
  totalGB: number
}
