import { z } from "zod";
import type { Invoice } from "../data/invoices.js";
import { requireScope } from "../auth/scope_guard.js";
import { auditToolCall } from "../observability/audit_log.js";
import type { MessageExtraInfo } from "@modelcontextprotocol/sdk/types.js";

export const REQUIRED_SCOPE = "invoices:read";

export const GetInvoiceStatusInput = z
  .object({
    invoiceId: z.string().regex(/^inv_[a-zA-Z0-9]+$/),
  })
  .strict();

export function getInvoiceStatusTool(invoices: Invoice[], authMode: "none" | "jwt") {
  return async (input: unknown, extra?: MessageExtraInfo) => {
    const start = Date.now();
    const parsed = GetInvoiceStatusInput.parse(input);

    try {
      const scopes = authMode === "jwt" ? requireScope(extra, REQUIRED_SCOPE) : [];
      const invoice = invoices.find((row) => row.invoice_id === parsed.invoiceId);

      if (!invoice) {
        auditToolCall({
          tool: "get_invoice_status",
          subject: String(extra?.authInfo?.clientId ?? "anonymous"),
          scopes,
          params: parsed,
          decision: "deny",
          latency_ms: Date.now() - start,
          error: "invoice_not_found",
        });

        return {
          content: [{ type: "text" as const, text: `Invoice not found: ${parsed.invoiceId}` }],
          isError: true,
        };
      }

      const payload = {
        invoice_id: invoice.invoice_id,
        account_id: invoice.account_id,
        status: invoice.status,
        amount: invoice.amount,
        currency: invoice.currency,
        due_date: invoice.due_date,
        updated_at: invoice.updated_at,
      };

      auditToolCall({
        tool: "get_invoice_status",
        subject: String(extra?.authInfo?.clientId ?? "anonymous"),
        scopes,
        params: parsed,
        decision: "allow",
        latency_ms: Date.now() - start,
      });

      return {
        content: [{ type: "text" as const, text: JSON.stringify(payload) }],
        structuredContent: payload,
      };
    } catch (error) {
      auditToolCall({
        tool: "get_invoice_status",
        subject: String(extra?.authInfo?.clientId ?? "anonymous"),
        scopes: extra?.authInfo?.scopes ?? [],
        params: parsed,
        decision: "deny",
        latency_ms: Date.now() - start,
        error: error instanceof Error ? error.message : "unknown_error",
      });
      throw error;
    }
  };
}
