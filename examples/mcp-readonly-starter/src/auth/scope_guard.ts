import type { MessageExtraInfo } from "@modelcontextprotocol/sdk/types.js";

export function requireScope(extra: MessageExtraInfo | undefined, required: string): string[] {
  const scopes = extra?.authInfo?.scopes ?? [];
  if (!scopes.includes(required)) {
    throw new Error(`forbidden: missing scope ${required}`);
  }
  return scopes;
}
