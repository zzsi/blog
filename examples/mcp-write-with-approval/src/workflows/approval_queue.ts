export type RefundRequest = {
  requestId: string;
  orderId: string;
  amountCents: number;
  reason: string;
  createdBy: string;
  status: "pending_approval" | "approved" | "executed";
  requiresApproval: boolean;
  approverId?: string;
  approvedAt?: string;
  executedAt?: string;
};

export class RefundStore {
  private store = new Map<string, RefundRequest>();

  create(input: {
    orderId: string;
    amountCents: number;
    reason: string;
    createdBy: string;
    requiresApproval: boolean;
  }): RefundRequest {
    const requestId = `rr_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    const record: RefundRequest = {
      requestId,
      orderId: input.orderId,
      amountCents: input.amountCents,
      reason: input.reason,
      createdBy: input.createdBy,
      status: input.requiresApproval ? "pending_approval" : "approved",
      requiresApproval: input.requiresApproval,
      approverId: input.requiresApproval ? undefined : "auto-approval",
      approvedAt: input.requiresApproval ? undefined : new Date().toISOString(),
    };

    this.store.set(requestId, record);
    return record;
  }

  approve(requestId: string, approverId: string): RefundRequest {
    const record = this.getOrThrow(requestId);
    if (record.status !== "pending_approval") {
      throw new Error(`forbidden: request is ${record.status}, expected pending_approval`);
    }

    const updated: RefundRequest = {
      ...record,
      status: "approved",
      approverId,
      approvedAt: new Date().toISOString(),
    };
    this.store.set(requestId, updated);
    return updated;
  }

  execute(requestId: string): RefundRequest {
    const record = this.getOrThrow(requestId);
    if (record.status !== "approved") {
      throw new Error("forbidden: request not approved");
    }

    const updated: RefundRequest = {
      ...record,
      status: "executed",
      executedAt: new Date().toISOString(),
    };
    this.store.set(requestId, updated);
    return updated;
  }

  get(requestId: string): RefundRequest | undefined {
    return this.store.get(requestId);
  }

  private getOrThrow(requestId: string): RefundRequest {
    const record = this.store.get(requestId);
    if (!record) {
      throw new Error(`request_not_found: ${requestId}`);
    }
    return record;
  }
}

export function enqueueApproval(requestId: string) {
  return { requestId, status: "queued" as const };
}
