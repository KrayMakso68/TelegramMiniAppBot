export enum PaymentStatus {
  PENDING = "PENDING",
  COMPLETED = "COMPLETED",
  FAILED = "FAILED"
}

export enum OperationType {
  DEPOSIT = "DEPOSIT",
  WITHDRAWAL = "WITHDRAWAL"
}

export interface Payment {
  id: number,
  userId: number,
  amount: number,
  title?: string,
  status: PaymentStatus,
  operationType: OperationType,
  createdAt: Date,
  updatedAt: Date
}

export interface PaymentOptions {
  label: string,
  path: string
}
