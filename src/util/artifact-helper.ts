import { ArtifactSchema, FlatArtifact } from "@/types";

/**
 * Decides whether to filter an artifact out of view.
 *
 * @param artifact - The artifact to check.
 * @param queryText - The current query text.
 * @return If true, the artifact should be kept.
 */
export function filterArtifacts(
  artifact: ArtifactSchema,
  queryText: string
): boolean {
  const lowercaseQuery = queryText.toLowerCase();
  const { name, type, body } = artifact;

  return (
    name.toLowerCase().includes(lowercaseQuery) ||
    type.toLowerCase().includes(lowercaseQuery) ||
    body.toLowerCase().includes(lowercaseQuery)
  );
}

/**
 * Flattens an artifacts custom fields into the same object.
 *
 * @param artifact -The artifact to flatten.
 * @return The flattened artifact.
 */
export function flattenArtifact(artifact: ArtifactSchema): FlatArtifact {
  return {
    ...artifact,
    ...(artifact.attributes || {}),
  } as FlatArtifact;
}
