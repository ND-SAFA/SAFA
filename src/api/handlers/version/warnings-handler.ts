import { warningStore } from "@/hooks";
import { getWarningsInProjectVersion } from "@/api";

/**
 * Call this function whenever warnings need to be re-downloaded.
 *
 * @param versionId - The project version to load from.
 */
export async function handleReloadWarnings(versionId: string): Promise<void> {
  warningStore.artifactWarnings = await getWarningsInProjectVersion(versionId);
}
