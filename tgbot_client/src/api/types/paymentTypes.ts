enum PaymentStatus {
  PENDING = "PENDING",
  COMPLETED = "COMPLETED",
  FAILED = "FAILED"
}

enum OperationType {
  DEPOSIT = "DEPOSIT",
  WITHDRAWAL = "WITHDRAWAL"
}

export interface Payment {
  "id": number,
  "userId": number,
  "amount": number,
  "status": PaymentStatus,
  "operationType": OperationType,
  "createdAt": Date,
  "updatedAt": Date
}
