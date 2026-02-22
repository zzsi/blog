import { z } from "zod";
import type { MessageExtraInfo } from "@modelcontextprotocol/sdk/types.js";
import type { Invoice } from "../data/invoices.js";
import { requireTenantContext } from "../middleware/tenant_context.js";
import { requireTenantScope, REQUIRED_SCOPE } from "../middleware/authz.js";
import { logAuthzDecision } from "../observability/audit_log.js";

export const GetTenantInvoiceInput = z
  .object({
    invoiceId: z.string().regex(/^inv_[a-zA-Z0-9]+$/),
  })
  .strict();

export function getTenantInvoiceTool(invoices: Invoice[]) {
  return async (input: unknown, extra?: MessageExtraInfo) => {
    const start = Date.now();
    const parsed = GetTenantInvoiceInput.parse(input);
    const ctx = requireTenantContext(extra);

    const invoice = invoices.find((row) => row.invoice_id === parsed.invoiceId);
    if (!invoice) {
      logAuthzDecision({
        tool: "get_tenant_invoice",
        subject: ctx.subject,
        tenant_id: ctx.tenantId,
        scopes: ctx.scopes,
        params: parsed,
        decision: "deny",
        error: "invoice_not_found",
        latency_ms: Date.now() - start,
      });

      return {
        content: [{ type: "text" as const, text: `Invoice not found: ${parsed.invoiceId}` }],
        isError: true,
      };
    }

    requireTenantScope(ctx, REQUIRED_SCOPE, invoice.tenant_id);

    const payload = {
      invoice_id: invoice.invoice_id,
      account_id: invoice.account_id,
      tenant_id: invoice.tenant_id,
      status: invoice.status,
      amount: invoice.amount,
      currency: invoice.currency,
      due_date: invoice.due_date,
      updated_at: invoice.updated_at,
    };

    logAuthzDecision({
      tool: "get_tenant_invoice",
      subject: ctx.subject,
      tenant_id: ctx.tenantId,
      scopes: ctx.scopes,
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
