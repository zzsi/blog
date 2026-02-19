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
