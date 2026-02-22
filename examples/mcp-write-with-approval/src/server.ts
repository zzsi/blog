import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import * as z from "zod/v4";
import { RefundStore } from "./workflows/approval_queue.js";
import { createRefundRequestTool } from "./tools/create_refund_request.js";
import { approveRefundRequestTool } from "./tools/approve_refund_request.js";
import { executeRefundTool } from "./tools/execute_refund.js";

export function createServer(store: RefundStore = new RefundStore()) {

  const server = new McpServer(
    {
      name: "mcp-write-with-approval",
      version: "0.1.0",
    },
    {
      capabilities: { logging: {} },
    },
  );

  server.registerTool(
    "create_refund_request",
    {
      description: "Create a refund request (intent only)",
      inputSchema: {
        orderId: z.string().regex(/^ord_[a-zA-Z0-9]+$/),
        amountCents: z.number().int().positive().max(1_000_000_00),
        reason: z.string().min(5).max(500),
      },
    },
    async (args, extra) => createRefundRequestTool(store)(args, extra),
  );

  server.registerTool(
    "approve_refund_request",
    {
      description: "Approve a pending refund request",
      inputSchema: {
        requestId: z.string().regex(/^rr_[a-zA-Z0-9_]+$/),
      },
    },
    async (args, extra) => approveRefundRequestTool(store)(args, extra),
  );

  server.registerTool(
    "execute_refund",
    {
      description: "Execute an approved refund",
      inputSchema: {
        requestId: z.string().regex(/^rr_[a-zA-Z0-9_]+$/),
      },
    },
    async (args, extra) => executeRefundTool(store)(args, extra),
  );

  return server;
}
