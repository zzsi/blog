import { mkdirSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const stateFile = process.env.REFUND_STATE_FILE ?? ".demo-data/refund_requests.json";

const seeded = [
  {
    requestId: "rr_seed_0001",
    orderId: "ord_seed001",
    amountCents: 65000,
    reason: "Historical approved refund",
    createdBy: "seed-system",
    status: "executed",
    requiresApproval: true,
    approverId: "seed-approver",
    approvedAt: "2026-02-18T10:01:00Z",
    executedAt: "2026-02-18T10:03:00Z",
  },
];

mkdirSync(dirname(stateFile), { recursive: true });
writeFileSync(stateFile, `${JSON.stringify(seeded, null, 2)}\n`, "utf8");
process.stderr.write(`Seeded refund state at ${stateFile}\n`);
