import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import * as z from "zod/v4";
import { loadComplianceEvents } from "./data/audit_events.js";
import { getControlStatusTool } from "./tools/get_control_status.js";
import { listAuditEventsTool } from "./tools/list_audit_events.js";

export function createServer(authMode: "none" | "jwt") {
  const events = loadComplianceEvents();

  const server = new McpServer(
    {
      name: "mcp-compliance-audit",
      version: "0.1.0",
    },
    {
      capabilities: { logging: {} },
    },
  );

  server.registerTool(
    "list_audit_events",
    {
      description: "List redacted audit events with optional tenant and decision filters",
      inputSchema: {
        tenantId: z.string().regex(/^t[0-9]+$/).optional(),
        decision: z.enum(["allow", "deny"]).optional(),
        limit: z.number().int().min(1).max(50).default(10),
      },
    },
    async (args, extra) => listAuditEventsTool(events, authMode)(args, extra),
  );

  server.registerTool(
    "get_control_status",
    {
      description: "Return status for one compliance control",
      inputSchema: {
        controlId: z.enum(["log_redaction", "deny_by_default", "secret_rotation"]),
      },
    },
    async (args, extra) => getControlStatusTool(authMode)(args, extra),
  );

  return server;
}
