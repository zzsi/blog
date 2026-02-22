import { readFileSync } from "node:fs";
import { z } from "zod";

export const InvoiceRow = z.object({
  invoice_id: z.string(),
  account_id: z.string(),
  status: z.enum(["paid", "open", "overdue", "void"]),
  amount: z.coerce.number(),
  currency: z.string(),
  due_date: z.string(),
  updated_at: z.string(),
});

export type Invoice = z.infer<typeof InvoiceRow> & { tenant_id: string };

const DATASET_URL = new URL("../../../mcp-shared/data/invoices.csv", import.meta.url);

function parseCsvLine(line: string): string[] {
  return line.split(",").map((v) => v.trim());
}

function toTenant(accountId: string): string {
  const numeric = Number.parseInt(accountId.replace("acct_", ""), 10);
  if (Number.isNaN(numeric)) return "t3";
  if (numeric <= 13) return "t1";
  if (numeric <= 26) return "t2";
  return "t3";
}

export function loadInvoices(): Invoice[] {
  const text = readFileSync(DATASET_URL, "utf8");
  const lines = text.split(/\r?\n/).filter(Boolean);
  if (lines.length < 2) return [];

  const header = parseCsvLine(lines[0]);
  const rows: Invoice[] = [];

  for (const line of lines.slice(1)) {
    const values = parseCsvLine(line);
    const record: Record<string, string> = {};
    for (let i = 0; i < header.length; i += 1) {
      record[header[i]] = values[i] ?? "";
    }

    const invoice = InvoiceRow.parse(record);
    rows.push({ ...invoice, tenant_id: toTenant(invoice.account_id) });
  }

  return rows;
}

export function loadInvoicesFromFile(invoicesFile: string): Invoice[] {
  try {
    const text = readFileSync(invoicesFile, "utf8");
    const parsed = JSON.parse(text);
    if (!Array.isArray(parsed)) return [];
    return parsed.map((row) =>
      InvoiceRow.extend({ tenant_id: z.string() }).parse(row) as Invoice
    );
  } catch {
    return [];
  }
}
