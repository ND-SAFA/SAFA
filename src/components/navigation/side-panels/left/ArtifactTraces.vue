<template>
  <div v-if="parents.length + children.length > 0">
    <h2 class="text-h6">Trace Links</h2>
    <v-divider />

    <v-row>
      <v-col v-if="parents.length !== 0">
        <v-subheader style="height: 30px">Parents</v-subheader>
        <v-divider />
        <v-list dense style="max-height: 300px" class="overflow-y-auto">
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
                <span class="mb-1 text-ellipsis" :style="style">
                  {{ parentName }}
                </span>
              </v-btn>
            </template>
            <span> {{ parentName }}</span>
          </v-tooltip>
        </v-list>
      </v-col>

      <v-col v-if="children.length !== 0">
        <v-subheader style="height: 30px">Children</v-subheader>
        <v-divider />
        <v-list dense style="max-height: 300px" class="overflow-y-auto">
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
                <span class="mb-1 text-ellipsis" :style="style">
                  {{ childName }}
                </span>
              </v-btn>
            </template>
            <span> {{ childName }}</span>
          </v-tooltip>
        </v-list>
      </v-col>
    </v-row>
  </div>
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
    /**
     * Determines the width of trace link buttons.
     */
    style(): string {
      return this.children.length > 0 && this.parents.length > 0
        ? "max-width: 50px"
        : "max-width: 190px";
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
