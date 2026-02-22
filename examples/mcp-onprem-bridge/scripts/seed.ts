import { mkdirSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const stateFile = process.env.BRIDGE_STATE_FILE ?? ".demo-data/bridge_jobs.json";

const seeded = [
  {
    jobId: "job_seed_0001",
    requestId: "req_seed_0001",
    customerId: "cust_100",
    resource: "invoice",
    status: "completed",
    createdAt: "2026-02-18T08:00:00Z",
    updatedAt: "2026-02-18T08:01:00Z",
    result: {
      requestId: "req_seed_0001",
      customerId: "cust_100",
      resource: "invoice",
      data: { invoiceId: "inv_seed_20001", status: "paid", amountCents: 9000 },
    },
    idempotencyKey: "seed-cust100-invoice-001",
  },
];

mkdirSync(dirname(stateFile), { recursive: true });
writeFileSync(stateFile, `${JSON.stringify(seeded, null, 2)}\n`, "utf8");
process.stderr.write(`Seeded bridge state at ${stateFile}\n`);
