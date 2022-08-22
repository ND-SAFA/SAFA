<template>
  <v-container class="mt-2">
    <typography el="h1" variant="title" value="Artifact Hierarchy" />
    <v-divider class="mb-4" />

    <v-text-field
      label="Search Artifacts"
      outlined
      dense
      clearable
      append-icon="mdi-magnify"
      v-model="searchText"
      @click:clear="searchText = ''"
      hint="Search by artifact name or type"
    />

    <typography
      secondary
      el="div"
      variant="body"
      align="right"
      :value="searchHint"
    />

    <v-list class="search-container full-width" expand>
      <toggle-list
        v-for="type in artifactTypes"
        :key="type"
        :icon="getIconName(type)"
        :value="!!searchText"
      >
        <template v-slot:activator>
          <v-tooltip bottom open-delay="300">
            <template v-slot:activator="{ on, attrs }">
              <div v-on="on" v-bind="attrs">
                <typography :value="getTypePrintName(type)" />
                <typography
                  secondary
                  :value="`(${artifactTypeHashTable[type].length})`"
                />
              </div>
            </template>
            <span>
              {{ getTypePrintName(type) }}
              ({{ artifactTypeHashTable[type].length }})
            </span>
          </v-tooltip>
        </template>
        <v-list-item
          v-for="artifact in artifactTypeHashTable[type]"
          :key="artifact.name"
          @click="handleArtifactClick(artifact)"
        >
          <generic-artifact-body-display display-title :artifact="artifact" />
        </v-list-item>
      </toggle-list>
    </v-list>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { ArtifactModel } from "@/types";
import { filterArtifacts } from "@/util";
import { viewportModule, artifactModule } from "@/store";
import { typeOptionsStore } from "@/hooks";
import {
  Typography,
  GenericArtifactBodyDisplay,
  ToggleList,
} from "@/components/common";

/**
 * Displays all project artifacts.
 */
export default Vue.extend({
  name: "SubTreeSelectorTab",
  components: { Typography, GenericArtifactBodyDisplay, ToggleList },
  data() {
    return {
      searchText: "",
      artifacts: [] as ArtifactModel[],
      artifactTypes: [] as string[],
      artifactTypeHashTable: {} as Record<string, ArtifactModel[]>,
    };
  },
  mounted() {
    this.updateArtifacts();
  },
  computed: {
    /**
     * Returns how many results match.
     */
    searchHint(): string {
      return this.artifacts.length === 1
        ? "1 Match"
        : `${this.artifacts.length} Matches`;
    },
    /**
     * Returns all visible artifacts.
     */
    allArtifacts(): ArtifactModel[] {
      return artifactModule.artifacts;
    },
  },
  watch: {
    /**
     * Updates the currently displayed artifacts when the search changes.
     */
    searchText() {
      this.updateArtifacts();
    },
    /**
     * Updates the currently displayed artifacts when the artifacts change.
     */
    allArtifacts() {
      this.updateArtifacts();
    },
  },
  methods: {
    /**
     * Updates the saved list of artifacts to match the current search.
     */
    updateArtifacts(): void {
      const artifacts = artifactModule.artifacts;
      const hashTable: Record<string, ArtifactModel[]> = {};

      this.artifacts = this.searchText
        ? artifacts.filter((artifact) =>
            filterArtifacts(artifact, this.searchText)
          )
        : artifacts;

      this.artifacts.forEach((a) => {
        if (a.type in hashTable) {
          hashTable[a.type].push(a);
        } else {
          hashTable[a.type] = [a];
        }
      });

      this.artifactTypeHashTable = hashTable;
      this.artifactTypes = Object.keys(hashTable);
    },
    /**
     * Converts an artifact type into a title case name.
     * @param type - The artifact type.
     * @return The type display name.
     */
    getTypePrintName(type: string): string {
      return typeOptionsStore.getArtifactTypeDisplay(type);
    },
    /**
     * Returns the icon for this artifact type.
     * @param type - The artifact type.
     * @return The type icon.
     */
    getIconName(type: string): string {
      return typeOptionsStore.getArtifactTypeIcon(type);
    },
    /**
     * Focuses the graph on the given artifact's subtree.
     * @param artifact - The artifact focus on.
     */
    async handleArtifactClick(artifact: ArtifactModel): Promise<void> {
      await viewportModule.viewArtifactSubtree(artifact.id);
    },
  },
});
</script>

<style scoped>
.search-container {
  overflow-y: auto;
}
</style>
