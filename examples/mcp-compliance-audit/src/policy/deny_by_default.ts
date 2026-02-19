const POLICY: Record<string, readonly string[]> = {
  list_audit_events: ["compliance:audit:read"],
  get_control_status: ["compliance:control:read"],
};

export function authorizeTool(toolName: string, scopes: readonly string[]) {
  const requiredScopes = POLICY[toolName];
  if (!requiredScopes || requiredScopes.length === 0) {
    throw new Error(`forbidden: no policy for tool ${toolName}`);
  }

  for (const required of requiredScopes) {
    if (!scopes.includes(required)) {
      throw new Error(`forbidden: missing scope ${required}`);
    }
  }
}

export function authorize(allowed: boolean) {
  if (!allowed) throw new Error("forbidden");
}
