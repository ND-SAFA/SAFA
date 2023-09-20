import { defineStore } from "pinia";

import { SearchApiHook } from "@/types";
import { buildDocument } from "@/util";
import {
  useApi,
  documentStore,
  layoutStore,
  projectStore,
  searchStore,
} from "@/hooks";
import { getProjectSearchQuery } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing search API requests.
 */
export const useSearchApi = defineStore("searchApi", (): SearchApiHook => {
  const searchApi = useApi("searchApi");

  async function handleSearch(): Promise<void> {
    await searchApi.handleRequest(
      async () => {
        const searchQuery = searchStore.searchQuery;

        layoutStore.mode = "tree";

        const searchResults = await getProjectSearchQuery(
          projectStore.versionId,
          searchQuery
        );

        const document = buildDocument({
          project: projectStore.projectIdentifier,
          name: searchQuery.prompt || "Search Query",
          artifactIds: searchResults.artifactIds,
        });

        await documentStore.addDocument(document);
      },
      { useAppLoad: true, error: "Unable to display search results." }
    );
  }

  return { handleSearch };
});

export default useSearchApi(pinia);
