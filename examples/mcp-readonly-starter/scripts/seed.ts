import { mkdirSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";
import { loadInvoices } from "../src/data/invoices.js";

const invoicesFile = process.env.INVOICES_FILE ?? ".demo-data/invoices.json";
const invoices = loadInvoices();

mkdirSync(dirname(invoicesFile), { recursive: true });
writeFileSync(invoicesFile, `${JSON.stringify(invoices, null, 2)}\n`, "utf8");
process.stderr.write(`Seeded readonly invoices at ${invoicesFile} (${invoices.length} rows)\n`);
