export function requiresHumanApproval(amountCents: number): boolean {
  return amountCents >= 50000;
}
