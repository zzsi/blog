import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import * as z from "zod/v4";
import { loadInvoices } from "./data/invoices.js";
import { getTenantInvoiceTool } from "./tools/get_tenant_invoice.js";
import { listTenantOpenInvoicesTool } from "./tools/list_tenant_open_invoices.js";

export function createServer() {
  const invoices = loadInvoices();

  const server = new McpServer(
    {
      name: "mcp-multitenant-saas",
      version: "0.1.0",
    },
    {
      capabilities: { logging: {} },
    },
  );

  server.registerTool(
    "get_tenant_invoice",
    {
      description: "Get one invoice if it belongs to caller tenant",
      inputSchema: {
        invoiceId: z.string().regex(/^inv_[a-zA-Z0-9]+$/),
      },
    },
    async (args, extra) => getTenantInvoiceTool(invoices)(args, extra),
  );

  server.registerTool(
    "list_tenant_open_invoices",
    {
      description: "List open invoices for caller tenant",
      inputSchema: {
        limit: z.number().int().min(1).max(100).default(10),
      },
    },
    async (args, extra) => listTenantOpenInvoicesTool(invoices)(args, extra),
  );

  return server;
}
