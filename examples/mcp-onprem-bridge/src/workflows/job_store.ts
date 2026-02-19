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
};

export class BridgeJobStore {
  private jobs = new Map<string, BridgeJob>();
  private requestToJob = new Map<string, string>();
  private idempotencyToJob = new Map<string, string>();

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
    };

    this.jobs.set(jobId, job);
    this.requestToJob.set(requestId, jobId);
    if (input.idempotencyKey) {
      this.idempotencyToJob.set(input.idempotencyKey, jobId);
    }
    return { job, reused: false };
  }

  pullNextQueued(): BridgeJob | null {
    for (const job of this.jobs.values()) {
      if (job.status === "queued") {
        const updated: BridgeJob = { ...job, status: "processing", updatedAt: new Date().toISOString() };
        this.jobs.set(job.jobId, updated);
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
}
