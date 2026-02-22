import { z } from "zod";
import type { MessageExtraInfo } from "@modelcontextprotocol/sdk/types.js";
import { EXECUTE_SCOPE } from "../policy/risk_rules.js";
import { auditWorkflowEvent } from "../observability/audit_log.js";
import type { RefundStore } from "../workflows/approval_queue.js";

export const ExecuteRefundInput = z
  .object({
    requestId: z.string().regex(/^rr_[a-zA-Z0-9_]+$/),
  })
  .strict();

function requireExecutor(extra: MessageExtraInfo | undefined): string {
  const scopes = extra?.authInfo?.scopes ?? [];
  if (!scopes.includes(EXECUTE_SCOPE)) {
    throw new Error(`forbidden: missing scope ${EXECUTE_SCOPE}`);
  }
  return extra?.authInfo?.clientId ?? "unknown";
}

export function executeRefundTool(store: RefundStore) {
  return async (input: unknown, extra?: MessageExtraInfo) => {
    const parsed = ExecuteRefundInput.parse(input);
    const executor = requireExecutor(extra);
    const updated = store.execute(parsed.requestId);

    const payload = {
      requestId: updated.requestId,
      status: updated.status,
      approverId: updated.approverId,
      executedAt: updated.executedAt,
    };

    auditWorkflowEvent({
      action: "execute_refund",
      actor: executor,
      requestId: updated.requestId,
      status: updated.status,
    });

    return {
      content: [{ type: "text" as const, text: JSON.stringify(payload) }],
      structuredContent: payload,
    };
  };
}
