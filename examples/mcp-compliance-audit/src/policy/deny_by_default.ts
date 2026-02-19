export function authorize(allowed: boolean) {
  if (!allowed) throw new Error("forbidden");
}
