import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";
import type { OnPremResource } from "../data/mock_onprem_data.js";

export type BridgeJob = {
  jobId: string;
  requestId: string;
  customerId: string;
  resource: OnPremResource;
  status: "queued" | "processing" | "completed";
  createdAt: string;
  updatedAt: string;
  result?: unknown;
  idempotencyKey?: string;
};

export class BridgeJobStore {
  private jobs = new Map<string, BridgeJob>();
  private requestToJob = new Map<string, string>();
  private idempotencyToJob = new Map<string, string>();
  private readonly onChange?: (jobs: BridgeJob[]) => void;

  constructor(initial: BridgeJob[] = [], onChange?: (jobs: BridgeJob[]) => void) {
    for (const job of initial) {
      this.jobs.set(job.jobId, job);
      this.requestToJob.set(job.requestId, job.jobId);
      if (job.idempotencyKey) {
        this.idempotencyToJob.set(job.idempotencyKey, job.jobId);
      }
    }
    this.onChange = onChange;
  }

  create(input: { customerId: string; resource: OnPremResource }): BridgeJob {
    return this.createOrReuse(input).job;
  }

  createOrReuse(input: { customerId: string; resource: OnPremResource; idempotencyKey?: string }): { job: BridgeJob; reused: boolean } {
    if (input.idempotencyKey) {
      const existingJobId = this.idempotencyToJob.get(input.idempotencyKey);
      if (existingJobId) {
        const existingJob = this.jobs.get(existingJobId);
        if (existingJob) {
          return { job: existingJob, reused: true };
        }
      }
    }

    const requestId = `req_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    const jobId = `job_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    const now = new Date().toISOString();

    const job: BridgeJob = {
      jobId,
      requestId,
      customerId: input.customerId,
      resource: input.resource,
      status: "queued",
      createdAt: now,
      updatedAt: now,
      idempotencyKey: input.idempotencyKey,
    };

    this.jobs.set(jobId, job);
    this.requestToJob.set(requestId, jobId);
    if (input.idempotencyKey) {
      this.idempotencyToJob.set(input.idempotencyKey, jobId);
    }
    this.persist();
    return { job, reused: false };
  }

  pullNextQueued(): BridgeJob | null {
    for (const job of this.jobs.values()) {
      if (job.status === "queued") {
        const updated: BridgeJob = { ...job, status: "processing", updatedAt: new Date().toISOString() };
        this.jobs.set(job.jobId, updated);
        this.persist();
        return updated;
      }
    }
    return null;
  }

  complete(jobId: string, result: unknown): BridgeJob {
    const job = this.jobs.get(jobId);
    if (!job) throw new Error(`job_not_found: ${jobId}`);
    const updated: BridgeJob = {
      ...job,
      status: "completed",
      result,
      updatedAt: new Date().toISOString(),
    };
    this.jobs.set(jobId, updated);
    this.persist();
    return updated;
  }

  getByRequestId(requestId: string): BridgeJob | undefined {
    const jobId = this.requestToJob.get(requestId);
    if (!jobId) return undefined;
    return this.jobs.get(jobId);
  }

  getStats() {
    const values = Array.from(this.jobs.values());
    let queued = 0;
    let processing = 0;
    let completed = 0;
    let oldestQueuedCreatedAt: string | null = null;

    for (const job of values) {
      if (job.status === "queued") {
        queued += 1;
        if (!oldestQueuedCreatedAt || job.createdAt < oldestQueuedCreatedAt) {
          oldestQueuedCreatedAt = job.createdAt;
        }
      } else if (job.status === "processing") {
        processing += 1;
      } else if (job.status === "completed") {
        completed += 1;
      }
    }

    const oldestQueuedAgeMs = oldestQueuedCreatedAt
      ? Math.max(0, Date.now() - new Date(oldestQueuedCreatedAt).getTime())
      : null;

    return {
      totalJobs: values.length,
      queued,
      processing,
      completed,
      oldestQueuedAgeMs,
    };
  }

  private persist() {
    this.onChange?.(Array.from(this.jobs.values()));
  }
}

function parseJobs(input: unknown): BridgeJob[] {
  if (!Array.isArray(input)) return [];
  const out: BridgeJob[] = [];
  for (const row of input) {
    if (!row || typeof row !== "object") continue;
    const job = row as Partial<BridgeJob>;
    if (typeof job.jobId !== "string") continue;
    if (typeof job.requestId !== "string") continue;
    if (typeof job.customerId !== "string") continue;
    if (job.resource !== "invoice" && job.resource !== "contract") continue;
    if (job.status !== "queued" && job.status !== "processing" && job.status !== "completed") continue;
    if (typeof job.createdAt !== "string" || typeof job.updatedAt !== "string") continue;
    out.push({
      jobId: job.jobId,
      requestId: job.requestId,
      customerId: job.customerId,
      resource: job.resource,
      status: job.status,
      createdAt: job.createdAt,
      updatedAt: job.updatedAt,
      result: job.result,
      idempotencyKey: job.idempotencyKey,
    });
  }
  return out;
}

export function createFileBackedBridgeJobStore(stateFile: string): BridgeJobStore {
  let initial: BridgeJob[] = [];
  try {
    const text = readFileSync(stateFile, "utf8");
    initial = parseJobs(JSON.parse(text));
  } catch {
    initial = [];
  }

  return new BridgeJobStore(initial, (jobs) => {
    mkdirSync(dirname(stateFile), { recursive: true });
    writeFileSync(stateFile, `${JSON.stringify(jobs, null, 2)}\n`, "utf8");
  });
}
