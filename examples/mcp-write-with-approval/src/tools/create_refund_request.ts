import { z } from "zod";
import type { MessageExtraInfo } from "@modelcontextprotocol/sdk/types.js";
import { auditWorkflowEvent } from "../observability/audit_log.js";
import { REQUEST_SCOPE, requiresHumanApproval } from "../policy/risk_rules.js";
import type { RefundStore } from "../workflows/approval_queue.js";

export const CreateRefundRequestInput = z
  .object({
    orderId: z.string().regex(/^ord_[a-zA-Z0-9]+$/),
    amountCents: z.number().int().positive().max(1_000_000_00),
    reason: z.string().min(5).max(500),
  })
  .strict();

function requireScope(extra: MessageExtraInfo | undefined, requiredScope: string): string {
  const scopes = extra?.authInfo?.scopes ?? [];
  if (!scopes.includes(requiredScope)) {
    throw new Error(`forbidden: missing scope ${requiredScope}`);
  }

  return extra?.authInfo?.clientId ?? "unknown";
}

export function createRefundRequestTool(store: RefundStore) {
  return async (input: unknown, extra?: MessageExtraInfo) => {
    const parsed = CreateRefundRequestInput.parse(input);
    const caller = requireScope(extra, REQUEST_SCOPE);
    const needsApproval = requiresHumanApproval(parsed.amountCents);
    const record = store.create({
      ...parsed,
      createdBy: caller,
      requiresApproval: needsApproval,
    });

    const payload = {
      requestId: record.requestId,
      status: record.status,
      requiresApproval: record.requiresApproval,
      orderId: record.orderId,
      amountCents: record.amountCents,
      reason: record.reason,
      createdBy: record.createdBy,
    };

    auditWorkflowEvent({
      action: "create_refund_request",
      actor: caller,
      requestId: record.requestId,
      status: record.status,
      requiresApproval: record.requiresApproval,
      amountCents: record.amountCents,
    });

    return {
      content: [{ type: "text" as const, text: JSON.stringify(payload) }],
      structuredContent: payload,
    };
  };
}
