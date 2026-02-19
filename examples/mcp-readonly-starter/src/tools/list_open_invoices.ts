import { z } from "zod";
import type { Invoice } from "../data/invoices.js";
import { requireScope } from "../auth/scope_guard.js";
import { auditToolCall } from "../observability/audit_log.js";
import type { MessageExtraInfo } from "@modelcontextprotocol/sdk/types.js";
import { REQUIRED_SCOPE } from "./get_invoice_status.js";

export const ListOpenInvoicesInput = z
  .object({
    accountId: z.string().regex(/^acct_[a-zA-Z0-9]+$/).optional(),
    limit: z.number().int().min(1).max(100).default(10),
  })
  .strict();

export function listOpenInvoicesTool(invoices: Invoice[], authMode: "none" | "jwt") {
  return async (input: unknown, extra?: MessageExtraInfo) => {
    const start = Date.now();
    const parsed = ListOpenInvoicesInput.parse(input ?? {});

    try {
      const scopes = authMode === "jwt" ? requireScope(extra, REQUIRED_SCOPE) : [];

      const filtered = invoices
        .filter((row) => row.status === "open")
        .filter((row) => (parsed.accountId ? row.account_id === parsed.accountId : true))
        .slice(0, parsed.limit)
        .map((row) => ({
          invoice_id: row.invoice_id,
          account_id: row.account_id,
          status: row.status,
          amount: row.amount,
          currency: row.currency,
          due_date: row.due_date,
          updated_at: row.updated_at,
        }));

      const payload = {
        count: filtered.length,
        invoices: filtered,
      };

      auditToolCall({
        tool: "list_open_invoices",
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
        tool: "list_open_invoices",
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
