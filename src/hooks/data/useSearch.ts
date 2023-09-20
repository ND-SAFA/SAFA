import { defineStore } from "pinia";

import {
  ArtifactSchema,
  GenerationModelSchema,
  SearchQuerySchema,
} from "@/types";
import { searchModeOptions } from "@/util";
import { pinia } from "@/plugins";

/**
 * This module defines the state of the project searchbar.
 */
export const useSearch = defineStore("search", {
  state: () => ({
    /**
     * The type of information to predict traces to.
     */
    mode: searchModeOptions()[2],
    /**
     * The selected search items, used as the search artifacts and types.
     */
    searchItems: null as ArtifactSchema[] | string[] | null,
    /**
     * The inputted search text, used as the search prompt.
     */
    searchText: "",
    /**
     * What type(s) of artifacts to predict links from the search artifacts to.
     */
    searchTypes: [] as string[],
    /**
     * The generation model to use for the search.
     */
    searchModel: undefined as GenerationModelSchema | undefined,
    /**
     * How many of the top predictions to include.
     */
    maxResults: 5,
    /**
     * What other type(s) of artifacts should I import.
     */
    relatedTypes: [] as string[],
  }),
  getters: {
    /**
     * Whether the search mode searches for artifacts.
     */
    artifactLikeMode(): boolean {
      return !!this.mode.artifactSearch;
    },
    /**
     * Whether the search mode searches for artifact types.
     */
    artifactTypeMode(): boolean {
      return this.mode.id === "artifactTypes";
    },
    /**
     * Whether the search mode is basic search.
     */
    basicSearchMode(): boolean {
      return this.mode.id === "search";
    },
    /**
     * The number of search items selected.
     */
    selectionCount(): number {
      return this.searchItems?.length || 0;
    },
    /**
     * The ids of selected artifacts or types.
     */
    selectionIds(): string[] {
      return (
        this.searchItems?.map((item) =>
          typeof item === "object" ? item.id : item || ""
        ) || []
      );
    },
    /**
     * Builds the search query based on entered information.
     */
    searchQuery(): SearchQuerySchema {
      const searchQuery: SearchQuerySchema = {
        mode: this.mode.id,
        searchTypes: this.searchTypes,
        maxResults: this.maxResults,
        relatedTypes: this.relatedTypes,
        model: this.searchModel?.id,
      };

      if (this.mode.id === "prompt") {
        searchQuery.prompt = this.searchText;
      } else if (this.mode.id === "artifacts") {
        searchQuery.artifactIds = this.selectionIds;
      } else {
        searchQuery.artifactTypes = this.selectionIds;
      }

      return searchQuery;
    },
  },
  actions: {
    /**
     * Clears the search inputs.
     */
    clearSearch(): void {
      this.searchItems = [];
      this.searchText = "";
      this.searchTypes = [];
      this.relatedTypes = [];
    },
  },
});

export default useSearch(pinia);
