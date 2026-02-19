import { z } from "zod";
import type { MessageExtraInfo } from "@modelcontextprotocol/sdk/types.js";
import type { Invoice } from "../data/invoices.js";
import { requireTenantContext } from "../middleware/tenant_context.js";
import { REQUIRED_SCOPE } from "../middleware/authz.js";
import { logAuthzDecision } from "../observability/audit_log.js";

export const ListTenantOpenInvoicesInput = z
  .object({
    limit: z.number().int().min(1).max(100).default(10),
  })
  .strict();

export function listTenantOpenInvoicesTool(invoices: Invoice[]) {
  return async (input: unknown, extra?: MessageExtraInfo) => {
    const start = Date.now();
    const parsed = ListTenantOpenInvoicesInput.parse(input ?? {});
    const ctx = requireTenantContext(extra);

    if (!ctx.scopes.includes(REQUIRED_SCOPE)) {
      throw new Error("forbidden: missing scope");
    }

    const tenantInvoices = invoices
      .filter((row) => row.tenant_id === ctx.tenantId)
      .filter((row) => row.status === "open")
      .slice(0, parsed.limit)
      .map((row) => ({
        invoice_id: row.invoice_id,
        account_id: row.account_id,
        tenant_id: row.tenant_id,
        status: row.status,
        amount: row.amount,
        currency: row.currency,
        due_date: row.due_date,
        updated_at: row.updated_at,
      }));

    const payload = { count: tenantInvoices.length, invoices: tenantInvoices };

    logAuthzDecision({
      tool: "list_tenant_open_invoices",
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
