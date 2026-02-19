import type { BridgeJobStore } from "../workflows/job_store.js";
import { signPayload, verifyPayloadSignature } from "../security/job_signing.js";
import { auditEvent } from "../observability/audit_log.js";

export function requireBridgeAgentToken(expectedToken: string) {
  return (req: any, res: any, next: any) => {
    const auth = req.headers.authorization ?? "";
    const token = auth.startsWith("Bearer ") ? auth.slice("Bearer ".length) : "";
    if (token !== expectedToken) {
      res.status(401).json({ error: "unauthorized_bridge_agent" });
      return;
    }
    next();
  };
}

export function createBridgeHandlers(store: BridgeJobStore, jobSigningSecret: string) {
  const pullJob = (_req: any, res: any) => {
    const job = store.pullNextQueued();
    if (!job) {
      res.status(204).end();
      return;
    }

    const payload = {
      jobId: job.jobId,
      requestId: job.requestId,
      customerId: job.customerId,
      resource: job.resource,
      issuedAt: new Date().toISOString(),
    };

    const signature = signPayload(payload, jobSigningSecret);
    auditEvent({ action: "bridge_job_pulled", jobId: job.jobId, requestId: job.requestId });
    res.json({ payload, signature });
  };

  const postResult = (req: any, res: any) => {
    const jobId = req.params.jobId;
    const signature = String(req.body?.signature ?? "");
    const result = req.body?.result;

    const valid = verifyPayloadSignature({ jobId, result }, jobSigningSecret, signature);
    if (!valid) {
      res.status(400).json({ error: "invalid_result_signature" });
      return;
    }

    const updated = store.complete(jobId, result);
    auditEvent({ action: "bridge_result_received", jobId: updated.jobId, requestId: updated.requestId });
    res.json({ ok: true, status: updated.status });
  };

  return { pullJob, postResult };
}
