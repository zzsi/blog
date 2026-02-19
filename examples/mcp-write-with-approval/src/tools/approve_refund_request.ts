import { z } from "zod";
import type { MessageExtraInfo } from "@modelcontextprotocol/sdk/types.js";
import { APPROVE_SCOPE } from "../policy/risk_rules.js";
import { auditWorkflowEvent } from "../observability/audit_log.js";
import type { RefundStore } from "../workflows/approval_queue.js";

export const ApproveRefundRequestInput = z
  .object({
    requestId: z.string().regex(/^rr_[a-zA-Z0-9_]+$/),
  })
  .strict();

function requireApprover(extra: MessageExtraInfo | undefined): string {
  const scopes = extra?.authInfo?.scopes ?? [];
  if (!scopes.includes(APPROVE_SCOPE)) {
    throw new Error(`forbidden: missing scope ${APPROVE_SCOPE}`);
  }
  return extra?.authInfo?.clientId ?? "unknown";
}

export function approveRefundRequestTool(store: RefundStore) {
  return async (input: unknown, extra?: MessageExtraInfo) => {
    const parsed = ApproveRefundRequestInput.parse(input);
    const approverId = requireApprover(extra);
    const updated = store.approve(parsed.requestId, approverId);

    const payload = {
      requestId: updated.requestId,
      status: updated.status,
      approverId: updated.approverId,
      approvedAt: updated.approvedAt,
    };

    auditWorkflowEvent({
      action: "approve_refund_request",
      actor: approverId,
      requestId: updated.requestId,
      status: updated.status,
    });

    return {
      content: [{ type: "text" as const, text: JSON.stringify(payload) }],
      structuredContent: payload,
    };
  };
}
