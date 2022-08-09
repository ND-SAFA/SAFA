import { Artifact } from "@/types";

/**
 * Decides whether to filter an artifact out of view.
 *
 * @param artifact - The artifact to check.
 * @param queryText - The current query text.
 * @return If true, the artifact should be kept.
 */
export function filterArtifacts(
  artifact: Artifact,
  queryText: string
): boolean {
  const lowercaseQuery = queryText.toLowerCase();
  const { name, type } = artifact;

  return (
    name.toLowerCase().includes(lowercaseQuery) ||
    type.toLowerCase().includes(lowercaseQuery) ||
    type.toLowerCase().includes(lowercaseQuery)
  );
}
