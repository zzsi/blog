import type { MessageExtraInfo } from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";
import { writeAuditLog } from "../observability/audit_logger.js";
import { authorizeTool } from "../policy/deny_by_default.js";
import { getSecret } from "../secrets/adapter.js";

const Input = z.object({
  controlId: z.enum(["log_redaction", "deny_by_default", "secret_rotation"]),
}).strict();

const CONTROL_STATE = {
  log_redaction: {
    status: "pass",
    evidence: "redaction middleware active",
  },
  deny_by_default: {
    status: "pass",
    evidence: "tool allow matrix enforced",
  },
  secret_rotation: {
    status: "monitor",
    evidence: "rotation window configured",
  },
} as const;

function resolveScopes(extra: MessageExtraInfo | undefined): string[] {
  return extra?.authInfo?.scopes ?? [];
}

export function getControlStatusTool(authMode: "none" | "jwt") {
  return async (input: unknown, extra?: MessageExtraInfo) => {
    const start = Date.now();
    const parsed = Input.parse(input);
    const scopes = resolveScopes(extra);

    if (authMode === "jwt") {
      authorizeTool("get_control_status", scopes);
    }

    const state = CONTROL_STATE[parsed.controlId];
    const secretRef = `SECRET_${parsed.controlId.toUpperCase()}`;
    // Access goes through the central adapter; actual value is never returned.
    getSecret(parsed.controlId);

    const payload = {
      controlId: parsed.controlId,
      status: state.status,
      evidence: state.evidence,
      secretRef,
    };

    writeAuditLog({
      action: "get_control_status",
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
