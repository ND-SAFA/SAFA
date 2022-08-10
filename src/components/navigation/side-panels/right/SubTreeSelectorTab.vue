<template>
  <v-container>
    <h1 class="text-h4 my-2">Artifact Hierarchy</h1>
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

    <div class="full-width text-right text-subtitle-1 text--secondary">
      {{ searchHint }}
    </div>

    <v-list class="search-container full-width" expand>
      <v-list-group
        v-for="type in artifactTypes"
        :key="type"
        :prepend-icon="getIconName(type)"
        :value="!!searchText"
      >
        <template v-slot:activator>
          <v-list-item-title>
            <v-tooltip bottom open-delay="300">
              <template v-slot:activator="{ on, attrs }">
                <div v-on="on" v-bind="attrs">
                  <span class="text-body-1">
                    {{ getTypePrintName(type) }}
                  </span>
                  <span class="text-subtitle-1 text--secondary ml-1">
                    ({{ artifactTypeHashTable[type].length }})
                  </span>
                </div>
              </template>
              <span>
                {{ getTypePrintName(type) }}
                ({{ artifactTypeHashTable[type].length }})
              </span>
            </v-tooltip>
          </v-list-item-title>
        </template>
        <v-divider />
        <v-list-item
          v-for="artifact in artifactTypeHashTable[type]"
          :key="artifact.name"
          @click="handleArtifactClick(artifact)"
        >
          <v-list-item-content>
            <v-list-item-title>{{ artifact.name }}</v-list-item-title>

            <v-list-item-subtitle
              class="text-wrap text-ellipsis"
              style="max-height: 100px"
            >
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
import { filterArtifacts, getArtifactTypePrintName } from "@/util";
import { typeOptionsModule, viewportModule, artifactModule } from "@/store";

/**
 * Displays all project artifacts.
 */
export default Vue.extend({
  name: "SubTreeSelectorTab",
  data() {
    return {
      searchText: "",
      artifacts: [] as Artifact[],
      artifactTypes: [] as string[],
      artifactTypeHashTable: {} as Record<string, Artifact[]>,
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
    allArtifacts(): Artifact[] {
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
      const hashTable: Record<string, Artifact[]> = {};

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
