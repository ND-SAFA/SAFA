import { ArtifactData } from "@/types";

/**
 * Returns the number of parent and child warnings for an artifact.
 *
 * @param data - The artifact data to render.
 *
 * @return How many warnings to display.
 */
export function getWarnings(data: ArtifactData): number {
  const parentWarnings = data.warnings?.length || 0;
  const childWarnings = data.childWarnings?.length || 0;

  return data.hiddenChildren ? parentWarnings + childWarnings : parentWarnings;
}

/**
 * Returns the truncated text of an artifact.
 *
 * @param body - The artifact body text.
 * @param truncateLength - The number of characters to print before truncating.
 *
 * @return how many warnings to display.
 */
export function getBody(body: string, truncateLength: number): string {
  return body.length > truncateLength
    ? body.slice(0, truncateLength) + "..."
    : body;
}
