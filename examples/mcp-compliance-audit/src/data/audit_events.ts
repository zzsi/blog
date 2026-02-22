import { readFileSync } from "node:fs";

export type ComplianceEvent = {
  eventId: string;
  at: string;
  actor: string;
  tool: string;
  decision: "allow" | "deny";
  tenantId: string;
  metadata: Record<string, unknown>;
};

const EVENTS: ComplianceEvent[] = [
  {
    eventId: "evt_001",
    at: "2026-02-19T08:00:00Z",
    actor: "agent-ops-01",
    tool: "query_customer_data",
    decision: "allow",
    tenantId: "t1",
    metadata: {
      ticket: "SEC-3011",
      token: "top-secret-token",
      reason: "approved runbook",
    },
  },
  {
    eventId: "evt_002",
    at: "2026-02-19T08:02:00Z",
    actor: "agent-ops-02",
    tool: "execute_refund",
    decision: "deny",
    tenantId: "t1",
    metadata: {
      reason: "missing_scope",
      authorization: "Bearer super-secret",
    },
  },
  {
    eventId: "evt_003",
    at: "2026-02-19T08:03:00Z",
    actor: "auditor-01",
    tool: "list_audit_events",
    decision: "allow",
    tenantId: "t2",
    metadata: {
      ip: "10.22.1.15",
      note: "weekly review",
    },
  },
];

export function loadComplianceEvents(): ComplianceEvent[] {
  return EVENTS;
}

function parseEvents(input: unknown): ComplianceEvent[] {
  if (!Array.isArray(input)) return [];
  const out: ComplianceEvent[] = [];
  for (const row of input) {
    if (!row || typeof row !== "object") continue;
    const e = row as Partial<ComplianceEvent>;
    if (typeof e.eventId !== "string") continue;
    if (typeof e.at !== "string") continue;
    if (typeof e.actor !== "string") continue;
    if (typeof e.tool !== "string") continue;
    if (e.decision !== "allow" && e.decision !== "deny") continue;
    if (typeof e.tenantId !== "string") continue;
    if (!e.metadata || typeof e.metadata !== "object") continue;
    out.push({
      eventId: e.eventId,
      at: e.at,
      actor: e.actor,
      tool: e.tool,
      decision: e.decision,
      tenantId: e.tenantId,
      metadata: e.metadata as Record<string, unknown>,
    });
  }
  return out;
}

export function loadComplianceEventsFromFile(eventsFile: string): ComplianceEvent[] {
  try {
    const text = readFileSync(eventsFile, "utf8");
    return parseEvents(JSON.parse(text));
  } catch {
    return [];
  }
}
