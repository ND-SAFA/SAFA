<template>
  <v-row>
    <v-col>
      <v-subheader>Parents</v-subheader>
      <v-divider />
      <p v-if="parents.length === 0" class="text-caption text-center mt-1">
        No parents linked.
      </p>
      <v-list dense v-else>
        <v-tooltip bottom v-for="parentName in parents" :key="parentName">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-on="on"
              v-bind="attrs"
              outlined
              block
              class="mb-1"
              @click="handleArtifactClick(parentName)"
            >
              <span class="mb-1 text-ellipsis" style="max-width: 60px">
                {{ parentName }}
              </span>
            </v-btn>
          </template>
          <span> {{ parentName }}</span>
        </v-tooltip>
      </v-list>
    </v-col>

    <v-col>
      <v-subheader>Children</v-subheader>
      <v-divider />
      <p v-if="children.length === 0" class="text-caption text-center mt-1">
        No children linked.
      </p>
      <v-list dense v-else>
        <v-tooltip bottom v-for="childName in children" :key="childName">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-on="on"
              v-bind="attrs"
              outlined
              block
              class="mb-1"
              @click="handleArtifactClick(childName)"
            >
              <span class="mb-1 text-ellipsis" style="max-width: 60px">
                {{ childName }}
              </span>
            </v-btn>
          </template>
          <span> {{ childName }}</span>
        </v-tooltip>
      </v-list>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";
import { artifactModule, artifactSelectionModule, traceModule } from "@/store";

/**
 * Displays the selected node's parents and children.
 */
export default Vue.extend({
  name: "ArtifactTraces",
  computed: {
    /**
     * @return The selected artifact.
     */
    selectedArtifact() {
      return artifactSelectionModule.getSelectedArtifact;
    },
    /**
     * @return The selected artifact's parents.
     */
    parents(): string[] {
      if (!this.selectedArtifact) return [];

      return traceModule.traces
        .filter(({ sourceName }) => sourceName === this.selectedArtifact?.name)
        .map(({ targetName }) => targetName);
    },
    /**
     * @return The selected artifact's children.
     */
    children(): string[] {
      if (!this.selectedArtifact) return [];

      return traceModule.traces
        .filter(({ targetName }) => targetName === this.selectedArtifact?.name)
        .map(({ sourceName }) => sourceName);
    },
  },
  methods: {
    /**
     * Selects an artifact.
     * @param artifactName - The artifact to select.
     */
    handleArtifactClick(artifactName: string): void {
      const artifact = artifactModule.getArtifactByName(artifactName);

      artifactSelectionModule.selectArtifact(artifact.id);
    },
  },
});
</script>
