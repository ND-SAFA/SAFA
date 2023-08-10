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
    id: artifact.id,
    name: artifact.name,
    type: artifact.type,
    body: artifact.body,
    summary: artifact.summary || "",
    isCode: artifact.isCode || false,
    ...(artifact.attributes || {}),
  };
}

/**
 * Sorts a list of artifacts so that selected ones appear first.
 * @param artifacts - The list of artifacts to sort.
 * @param selectedIds - The list of selected artifact IDs.
 * @return The sorted list of artifacts.
 */
export function sortSelectedArtifactsToTop(
  artifacts: ArtifactSchema[],
  selectedIds: string[] | string | undefined | null
): ArtifactSchema[] {
  return [...artifacts].sort((a, b) => {
    // Move selected options to the top.
    if (selectedIds?.includes(a.id)) {
      return -1;
    } else if (selectedIds?.includes(b.id)) {
      return 1;
    }
    // Keep the original order for non-selected options.
    return artifacts.indexOf(a) - artifacts.indexOf(b);
  });
}
