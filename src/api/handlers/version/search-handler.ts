import { SearchMode } from "@/types";
import { layoutStore, searchStore, selectionStore } from "@/hooks";

export function handleProjectSearch(): void {
  const searchQuery = searchStore.searchQuery;

  console.log("searchQuery", searchQuery);

  if (
    searchQuery.mode === SearchMode.artifactTypes &&
    !!searchQuery.artifactTypes
  ) {
    selectionStore.selectArtifactLevel(searchQuery.artifactTypes[0]);
    layoutStore.viewTreeTypes(searchQuery.artifactTypes);
  } else if (
    searchQuery.mode === SearchMode.artifacts &&
    !!searchQuery.artifactIds
  ) {
    selectionStore.viewArtifactSubtree(searchQuery.artifactIds[0]);
  }
}
