<template>
  <v-container>
    <h1 class="text-h4 my-2">Artifact Hierarchy</h1>
    <v-col>
      <v-row>
        <v-text-field
          label="Search"
          solo
          rounded
          class="mt-5"
          dense
          prepend-inner-icon="mdi-magnify"
          v-model="searchText"
        />
      </v-row>
      <v-row>
        <v-list class="search-container">
          <v-list-group
            v-for="type in artifactTypes"
            :key="type"
            :prepend-icon="getIconName(type)"
          >
            <template v-slot:activator>
              <v-list-item-title>{{
                getTypePrintName(type)
              }}</v-list-item-title>
            </template>
            <v-list-item
              v-for="artifact in artifactTypeHashTable[type]"
              :key="artifact.name"
              @click="onArtifactClick(artifact)"
            >
              <v-list-item-content>
                <v-list-item-title>{{ artifact.name }}</v-list-item-title>

                <v-list-item-subtitle class="text-wrap">
                  {{ artifact.body }}</v-list-item-subtitle
                >
              </v-list-item-content>
            </v-list-item>
          </v-list-group>
        </v-list>
      </v-row>
    </v-col>
  </v-container>
</template>

<script lang="ts">
import { Artifact } from "@/types";
import Vue from "vue";
import { getArtifactTypePrintName } from "@/util";
import { projectModule, viewportModule } from "@/store";

export default Vue.extend({
  name: "artifact-tab",
  data() {
    return {
      searchText: "",
    };
  },
  methods: {
    getTypePrintName: getArtifactTypePrintName,
    getIconName(type: string): string {
      switch (type.toLowerCase()) {
        case "requirement":
          return "mdi-clipboard-text";
        case "design":
          return "mdi-math-compass";
        case "hazard":
          return "mdi-hazard-lights";
        case "environmentalassumption":
          return "mdi-pine-tree-fire";
        default:
          return "mdi-help";
      }
    },
    async onArtifactClick(artifact: Artifact): Promise<void> {
      await viewportModule.viewArtifactSubtree(artifact);
    },
  },
  computed: {
    artifacts(): Artifact[] {
      const artifacts: Artifact[] = projectModule.artifacts;
      if (this.searchText !== "") {
        return artifacts.filter((a) => a.body.includes(this.searchText));
      } else {
        return artifacts;
      }
    },
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
    artifactTypes(): string[] {
      return Object.keys(this.artifactTypeHashTable);
    },
  },
});
</script>

<style scoped>
.search-container {
  overflow-y: auto;
}
</style>
