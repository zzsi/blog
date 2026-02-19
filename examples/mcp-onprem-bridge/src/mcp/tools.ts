import { z } from "zod";
import type { MessageExtraInfo } from "@modelcontextprotocol/sdk/types.js";
import type { BridgeJobStore } from "../workflows/job_store.js";
import { auditEvent } from "../observability/audit_log.js";

const QUERY_SCOPE = "bridge:request";
const READ_SCOPE = "bridge:read";

const QueryInput = z.object({
  customerId: z.string().regex(/^cust_[0-9]+$/),
  resource: z.enum(["invoice", "contract"]),
  idempotencyKey: z.string().min(8).max(128).optional(),
}).strict();

const StatusInput = z.object({
  requestId: z.string().regex(/^req_[a-zA-Z0-9_]+$/),
}).strict();

function requireScope(extra: MessageExtraInfo | undefined, scope: string): string {
  const scopes = extra?.authInfo?.scopes ?? [];
  if (!scopes.includes(scope)) throw new Error(`forbidden: missing scope ${scope}`);
  return extra?.authInfo?.clientId ?? "unknown";
}

export function queryCustomerDataTool(store: BridgeJobStore) {
  return async (input: unknown, extra?: MessageExtraInfo) => {
    const parsed = QueryInput.parse(input);
    const caller = requireScope(extra, QUERY_SCOPE);
    const { job, reused } = store.createOrReuse({
      customerId: parsed.customerId,
      resource: parsed.resource,
      idempotencyKey: parsed.idempotencyKey,
    });

    auditEvent({
      action: reused ? "reuse_bridge_job" : "create_bridge_job",
      actor: caller,
      requestId: job.requestId,
      jobId: job.jobId,
      resource: job.resource,
      idempotencyKey: parsed.idempotencyKey ?? null,
    });

    const payload = {
      requestId: job.requestId,
      jobId: job.jobId,
      status: job.status,
      message: reused ? "duplicate_request_reused" : "queued_for_bridge",
      reused,
    };

    return { content: [{ type: "text" as const, text: JSON.stringify(payload) }], structuredContent: payload };
  };
}

export function getBridgeResultTool(store: BridgeJobStore) {
  return async (input: unknown, extra?: MessageExtraInfo) => {
    const parsed = StatusInput.parse(input);
    const caller = requireScope(extra, READ_SCOPE);
    const job = store.getByRequestId(parsed.requestId);

    if (!job) {
      return {
        content: [{ type: "text" as const, text: `request_not_found: ${parsed.requestId}` }],
        isError: true,
      };
    }

    auditEvent({ action: "read_bridge_result", actor: caller, requestId: parsed.requestId, status: job.status });

    const payload = {
      requestId: job.requestId,
      jobId: job.jobId,
      status: job.status,
      result: job.result ?? null,
    };

    return { content: [{ type: "text" as const, text: JSON.stringify(payload) }], structuredContent: payload };
  };
}
