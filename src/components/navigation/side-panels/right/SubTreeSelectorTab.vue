<template>
  <v-container>
    <h1 class="text-h4 my-2">Artifact Hierarchy</h1>
    <v-divider class="mb-4" />

    <v-text-field
      label="Search"
      solo
      rounded
      prepend-inner-icon="mdi-magnify"
      v-model="searchText"
    />

    <v-list class="search-container full-width">
      <v-list-group
        v-for="type in artifactTypes"
        :key="type"
        :prepend-icon="getIconName(type)"
      >
        <template v-slot:activator>
          <v-list-item-title>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <span v-on="on" v-bind="attrs">
                  {{ getTypePrintName(type) }}
                </span>
              </template>
              <span>{{ getTypePrintName(type) }}</span>
            </v-tooltip>
          </v-list-item-title>
        </template>
        <v-list-item
          v-for="artifact in artifactTypeHashTable[type]"
          :key="artifact.name"
          @click="handleArtifactClick(artifact)"
        >
          <v-list-item-content>
            <v-list-item-title>{{ artifact.name }}</v-list-item-title>

            <v-list-item-subtitle class="text-wrap">
              {{ artifact.body }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list-group>
    </v-list>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { Artifact } from "@/types";
import { getArtifactTypePrintName } from "@/util";
import { typeOptionsModule, viewportModule, artifactModule } from "@/store";

/**
 * Displays all project artifacts.
 */
export default Vue.extend({
  name: "SubTreeSelectorTab",
  data() {
    return {
      searchText: "",
    };
  },
  computed: {
    /**
     * @return Artifacts that match the search text.
     */
    artifacts(): Artifact[] {
      const artifacts = artifactModule.artifacts;
      const lowercaseSearch = this.searchText.toLowerCase();

      return lowercaseSearch
        ? artifacts.filter(
            ({ name, body }) =>
              name.toLowerCase().includes(lowercaseSearch) ||
              body.toLowerCase().includes(lowercaseSearch)
          )
        : artifacts;
    },
    /**
     * @return All artifacts grouped by their type.
     */
    artifactTypeHashTable(): Record<string, Artifact[]> {
      const hashTable: Record<string, Artifact[]> = {};

      this.artifacts.forEach((a) => {
        if (a.type in hashTable) {
          hashTable[a.type].push(a);
        } else {
          hashTable[a.type] = [a];
        }
      });

      return hashTable;
    },
    /**
     * @return All artifact types.
     */
    artifactTypes(): string[] {
      return Object.keys(this.artifactTypeHashTable);
    },
  },
  methods: {
    /**
     * Converts an artifact type into a title case name.
     * @param type - The artifact type.
     * @return The type display name.
     */
    getTypePrintName: getArtifactTypePrintName,
    /**
     * Returns the icon for this artifact type.
     * @param type - The artifact type.
     * @return The type icon.
     */
    getIconName(type: string): string {
      return typeOptionsModule.getArtifactTypeIcon(type);
    },
    /**
     * Focuses the graph on the given artifact's subtree.
     * @param artifact - The artifact focus on.
     */
    async handleArtifactClick(artifact: Artifact): Promise<void> {
      await viewportModule.viewArtifactSubtree(artifact);
    },
  },
});
</script>

<style scoped>
.search-container {
  overflow-y: auto;
}
</style>
