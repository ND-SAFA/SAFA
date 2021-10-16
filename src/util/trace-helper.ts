export function getTraceId(source: string, target: string): string {
  return `${source}-${target}`;
}
