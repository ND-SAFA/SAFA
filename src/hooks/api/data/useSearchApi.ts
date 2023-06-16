import { defineStore } from "pinia";

import { GraphMode } from "@/types";
import { createDocument } from "@/util";
import {
  useApi,
  documentStore,
  layoutStore,
  projectStore,
  searchStore,
} from "@/hooks";
import { getProjectSearchQuery } from "@/api";
import { pinia } from "@/plugins";

export const useSearchApi = defineStore("searchApi", () => {
  const searchApi = useApi("searchApi");

  /**
   * Handles searching a project, and updating the UI to display the search results.
   */
  async function handleSearch(): Promise<void> {
    await searchApi.handleRequest(
      async () => {
        const searchQuery = searchStore.searchQuery;

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
      },
      {},
      { useAppLoad: true, error: "Unable to display search results." }
    );
  }

  return { handleSearch };
});

export default useSearchApi(pinia);
