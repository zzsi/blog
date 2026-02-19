export async function pushResults(jobId: string, result: unknown) {
  // Stub: send minimized results back to control plane.
  return { jobId, uploaded: true, result };
}
