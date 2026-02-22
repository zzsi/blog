export const REQUEST_SCOPE = "refund:request";
export const APPROVE_SCOPE = "refund:approve";
export const EXECUTE_SCOPE = "refund:execute";

export function requiresHumanApproval(amountCents: number): boolean {
  return amountCents >= 50000;
}
