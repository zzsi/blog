export function enqueueApproval(requestId: string) {
  return { requestId, status: "queued" };
}
