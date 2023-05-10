import { createDocument } from "@/util";
import {
  appStore,
  documentStore,
  logStore,
  projectStore,
  searchStore,
} from "@/hooks";
import { getProjectSearchQuery } from "@/api";

/**
 * Handles searching a project, and updating the UI to display the search results.
 */
export async function handleProjectSearch(): Promise<void> {
  try {
    appStore.onLoadStart();

    const searchResults = await getProjectSearchQuery(
      projectStore.versionId,
      searchStore.searchQuery
    );

    const document = createDocument({
      project: projectStore.projectIdentifier,
      name: "Search Query",
      artifactIds: searchResults.artifactIds,
    });

    await documentStore.addDocument(document);
  } catch (e) {
    logStore.onError("Unable to display search results.");
  } finally {
    appStore.onLoadEnd();
  }
}
