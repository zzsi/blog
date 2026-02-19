import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import * as z from "zod/v4";
import { loadInvoices } from "./data/invoices.js";
import { getInvoiceStatusTool } from "./tools/get_invoice_status.js";
import { listOpenInvoicesTool } from "./tools/list_open_invoices.js";

export function createServer(authMode: "none" | "jwt") {
  const invoices = loadInvoices();

  const server = new McpServer(
    {
      name: "mcp-readonly-starter",
      version: "0.1.0",
    },
    {
      capabilities: { logging: {} },
    },
  );

  server.registerTool(
    "get_invoice_status",
    {
      description: "Get status and metadata for one invoice",
      inputSchema: {
        invoiceId: z.string().regex(/^inv_[a-zA-Z0-9]+$/),
      },
    },
    async (args, extra) => getInvoiceStatusTool(invoices, authMode)(args, extra),
  );

  server.registerTool(
    "list_open_invoices",
    {
      description: "List open invoices, optionally filtered by account ID",
      inputSchema: {
        accountId: z.string().regex(/^acct_[a-zA-Z0-9]+$/).optional(),
        limit: z.number().int().min(1).max(100).default(10),
      },
    },
    async (args, extra) => listOpenInvoicesTool(invoices, authMode)(args, extra),
  );

  server.registerResource(
    "invoice-dataset-info",
    "file:///dataset/invoices.csv",
    {
      title: "Synthetic invoice dataset metadata",
      mimeType: "application/json",
    },
    async () => ({
      contents: [
        {
          uri: "file:///dataset/invoices.csv",
          text: JSON.stringify({
            rows: invoices.length,
            source: "examples/mcp-shared/data/invoices.csv",
          }),
        },
      ],
    }),
  );

  return server;
}
