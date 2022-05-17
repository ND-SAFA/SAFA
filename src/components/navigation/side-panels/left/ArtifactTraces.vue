<template>
  <div v-if="parents.length + children.length > 0" class="mb-2">
    <div class="d-flex flex-row">
      <v-icon color="primary" style="transform: rotate(-45deg)">
        mdi-ray-start-arrow
      </v-icon>
      <h2 class="text-h6 ml-1">Trace Links</h2>
    </div>

    <v-divider class="mb-2" />

    <v-expansion-panels>
      <v-expansion-panel v-if="parents.length > 0">
        <v-expansion-panel-header class="text-body-1">
          {{ parentTitle }}
        </v-expansion-panel-header>
        <v-expansion-panel-content class="text-body-1">
          <v-list dense style="max-height: 300px" class="overflow-y-auto">
            <template v-for="(parentName, idx) in parents">
              <v-divider :key="parentName + '-div'" v-if="idx !== 0" />
              <v-tooltip
                bottom
                :key="parentName"
                :disabled="parentName.length < 30"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-list-item
                    v-on="on"
                    v-bind="attrs"
                    @click="handleArtifactClick(parentName)"
                  >
                    <v-list-item-title>
                      {{ parentName }}
                    </v-list-item-title>
                  </v-list-item>
                </template>
                <span> {{ parentName }}</span>
              </v-tooltip>
            </template>
          </v-list>
        </v-expansion-panel-content>
      </v-expansion-panel>

      <v-expansion-panel v-if="children.length > 0">
        <v-expansion-panel-header class="text-body-1">
          {{ childTitle }}
        </v-expansion-panel-header>
        <v-expansion-panel-content class="text-body-1">
          <v-list dense style="max-height: 300px" class="overflow-y-auto">
            <template v-for="(childName, idx) in children">
              <v-divider :key="childName + '-div'" v-if="idx !== 0" />
              <v-tooltip
                bottom
                :key="childName"
                :disabled="childName.length < 30"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-list-item
                    v-on="on"
                    v-bind="attrs"
                    @click="handleArtifactClick(childName)"
                  >
                    <v-list-item-title>
                      {{ childName }}
                    </v-list-item-title>
                  </v-list-item>
                </template>
                <span> {{ childName }}</span>
              </v-tooltip>
            </template>
          </v-list>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
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
        ? "max-width: 75px"
        : "max-width: 240px";
    },
    /**
     * Generates the name of the parent dropdown.
     */
    parentTitle(): string {
      const length = this.parents.length;

      return length === 1 ? "1 Parent" : `${length} Parents`;
    },
    /**
     * Generates the name of the child dropdown.
     */
    childTitle(): string {
      const length = this.children.length;

      return length === 1 ? "1 Child" : `${length} Children`;
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
