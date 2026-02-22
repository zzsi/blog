import { mkdirSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const eventsFile = process.env.COMPLIANCE_EVENTS_FILE ?? ".demo-data/compliance_events.json";

const events = [
  {
    eventId: "evt_seed_001",
    at: "2026-02-19T08:00:00Z",
    actor: "seed-ops-01",
    tool: "query_customer_data",
    decision: "allow",
    tenantId: "t1",
    metadata: {
      ticket: "SEC-SEED-001",
      token: "seed-sensitive-token",
      reason: "seeded demo event",
    },
  },
  {
    eventId: "evt_seed_002",
    at: "2026-02-19T08:02:00Z",
    actor: "seed-ops-02",
    tool: "execute_refund",
    decision: "deny",
    tenantId: "t1",
    metadata: {
      authorization: "Bearer seed-secret",
      reason: "seeded missing scope",
    },
  },
];

mkdirSync(dirname(eventsFile), { recursive: true });
writeFileSync(eventsFile, `${JSON.stringify(events, null, 2)}\n`, "utf8");
process.stderr.write(`Seeded compliance events at ${eventsFile}\n`);
