import { GraphMode } from "@/types";
import { createDocument } from "@/util";
import {
  appStore,
  documentStore,
  layoutStore,
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
    const searchQuery = searchStore.searchQuery;

    appStore.onLoadStart();

    layoutStore.mode = GraphMode.tree;

    const searchResults = await getProjectSearchQuery(
      projectStore.versionId,
      searchQuery
    );

    const document = createDocument({
      project: projectStore.projectIdentifier,
      name: searchQuery.prompt || "Search Query",
      artifactIds: searchResults.artifactIds,
    });

    await documentStore.addDocument(document);
  } catch (e) {
    logStore.onError("Unable to display search results.");
  } finally {
    appStore.onLoadEnd();
  }
}
