import type { MessageExtraInfo } from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";
import type { ComplianceEvent } from "../data/audit_events.js";
import { writeAuditLog } from "../observability/audit_logger.js";
import { redactValue } from "../observability/redaction.js";
import { authorizeTool } from "../policy/deny_by_default.js";

const Input = z.object({
  tenantId: z.string().regex(/^t[0-9]+$/).optional(),
  decision: z.enum(["allow", "deny"]).optional(),
  limit: z.number().int().min(1).max(50).default(10),
}).strict();

function resolveScopes(extra: MessageExtraInfo | undefined): string[] {
  return extra?.authInfo?.scopes ?? [];
}

export function listAuditEventsTool(events: ComplianceEvent[], authMode: "none" | "jwt") {
  return async (input: unknown, extra?: MessageExtraInfo) => {
    const start = Date.now();
    const parsed = Input.parse(input);
    const scopes = resolveScopes(extra);

    if (authMode === "jwt") {
      authorizeTool("list_audit_events", scopes);
    }

    const filtered = events
      .filter((e) => (parsed.tenantId ? e.tenantId === parsed.tenantId : true))
      .filter((e) => (parsed.decision ? e.decision === parsed.decision : true))
      .slice(0, parsed.limit)
      .map((event) => redactValue(event));

    const payload = {
      count: filtered.length,
      events: filtered,
    };

    writeAuditLog({
      action: "list_audit_events",
      subject: extra?.authInfo?.clientId ?? "anonymous",
      scopes,
      params: parsed,
      decision: "allow",
      latency_ms: Date.now() - start,
    });

    return {
      content: [{ type: "text" as const, text: JSON.stringify(payload) }],
      structuredContent: payload,
    };
  };
}
