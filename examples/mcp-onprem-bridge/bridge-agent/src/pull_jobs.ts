export async function pullJobs(controlPlaneUrl: string) {
  // Stub: poll a signed job queue from control plane.
  return [{ jobId: "job_1", connector: "erp", queryTemplate: "invoice_by_id" }];
}
