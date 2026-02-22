import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

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
  private readonly onChange?: (records: RefundRequest[]) => void;

  constructor(initial: RefundRequest[] = [], onChange?: (records: RefundRequest[]) => void) {
    for (const record of initial) {
      this.store.set(record.requestId, record);
    }
    this.onChange = onChange;
  }

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
    this.persist();
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
    this.persist();
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
    this.persist();
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

  private persist() {
    this.onChange?.(Array.from(this.store.values()));
  }
}

export function enqueueApproval(requestId: string) {
  return { requestId, status: "queued" as const };
}

function parseRefundRecords(input: unknown): RefundRequest[] {
  if (!Array.isArray(input)) return [];
  const out: RefundRequest[] = [];
  for (const row of input) {
    if (!row || typeof row !== "object") continue;
    const rec = row as Partial<RefundRequest>;
    if (typeof rec.requestId !== "string") continue;
    if (typeof rec.orderId !== "string") continue;
    if (typeof rec.amountCents !== "number") continue;
    if (typeof rec.reason !== "string") continue;
    if (typeof rec.createdBy !== "string") continue;
    if (rec.status !== "pending_approval" && rec.status !== "approved" && rec.status !== "executed") continue;
    if (typeof rec.requiresApproval !== "boolean") continue;
    out.push({
      requestId: rec.requestId,
      orderId: rec.orderId,
      amountCents: rec.amountCents,
      reason: rec.reason,
      createdBy: rec.createdBy,
      status: rec.status,
      requiresApproval: rec.requiresApproval,
      approverId: rec.approverId,
      approvedAt: rec.approvedAt,
      executedAt: rec.executedAt,
    });
  }
  return out;
}

export function createFileBackedRefundStore(stateFile: string): RefundStore {
  let initial: RefundRequest[] = [];

  try {
    const text = readFileSync(stateFile, "utf8");
    initial = parseRefundRecords(JSON.parse(text));
  } catch {
    initial = [];
  }

  return new RefundStore(initial, (records) => {
    mkdirSync(dirname(stateFile), { recursive: true });
    writeFileSync(stateFile, `${JSON.stringify(records, null, 2)}\n`, "utf8");
  });
}
