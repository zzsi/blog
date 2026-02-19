import { loadConfig } from "./config/index.js";
import { verifyPayloadSignature, signPayload } from "./security/job_signing.js";
import { readOnPremResource } from "./data/mock_onprem_data.js";

const config = loadConfig();

async function pullJob(baseUrl: string, token: string) {
  const res = await fetch(`${baseUrl}/bridge/jobs/pull`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });

  if (res.status === 204) return null;
  if (!res.ok) throw new Error(`pull_failed: ${res.status}`);

  return await res.json() as {
    payload: { jobId: string; requestId: string; customerId: string; resource: "invoice" | "contract"; issuedAt: string };
    signature: string;
  };
}

async function postResult(baseUrl: string, token: string, jobId: string, result: unknown, secret: string) {
  const signature = signPayload({ jobId, result }, secret);
  const res = await fetch(`${baseUrl}/bridge/jobs/${jobId}/result`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ result, signature }),
  });

  if (!res.ok) {
    throw new Error(`post_result_failed: ${res.status}`);
  }
}

async function runOnce() {
  const pulled = await pullJob(config.controlPlaneUrl, config.bridgeAgentToken);
  if (!pulled) {
    process.stderr.write("bridge-agent: no queued job\n");
    return;
  }

  const ok = verifyPayloadSignature(pulled.payload, config.jobSigningSecret, pulled.signature);
  if (!ok) throw new Error("invalid_control_plane_signature");

  const minimized = {
    requestId: pulled.payload.requestId,
    customerId: pulled.payload.customerId,
    resource: pulled.payload.resource,
    data: readOnPremResource(pulled.payload.customerId, pulled.payload.resource),
  };

  await postResult(config.controlPlaneUrl, config.bridgeAgentToken, pulled.payload.jobId, minimized, config.jobSigningSecret);
  process.stderr.write(`bridge-agent: processed ${pulled.payload.jobId}\n`);
}

async function main() {
  const once = process.argv.includes("--once");
  if (once) {
    await runOnce();
    return;
  }

  process.stderr.write(`bridge-agent: polling ${config.controlPlaneUrl} every ${config.bridgePollIntervalMs}ms\n`);
  for (;;) {
    try {
      await runOnce();
    } catch (error) {
      process.stderr.write(`bridge-agent error: ${String(error)}\n`);
    }
    await new Promise((resolve) => setTimeout(resolve, config.bridgePollIntervalMs));
  }
}

main().catch((error) => {
  process.stderr.write(`bridge-agent fatal: ${String(error)}\n`);
  process.exit(1);
});
