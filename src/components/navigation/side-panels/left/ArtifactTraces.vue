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
        <v-expansion-panel-content>
          <v-list dense style="max-height: 300px" class="overflow-y-auto">
            <template v-for="(parent, idx) in parents">
              <v-divider :key="parent.title + '-div'" v-if="idx !== 0" />
              <generic-list-item
                :key="parent.title"
                :item="parent"
                @click="handleArtifactClick(parent.title)"
              />
            </template>
          </v-list>
        </v-expansion-panel-content>
      </v-expansion-panel>

      <v-expansion-panel v-if="children.length > 0">
        <v-expansion-panel-header class="text-body-1">
          {{ childTitle }}
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-list dense style="max-height: 300px" class="overflow-y-auto">
            <template v-for="(child, idx) in children">
              <v-divider :key="child.title + '-div'" v-if="idx !== 0" />
              <generic-list-item
                :key="child.title"
                :item="child"
                @click="handleArtifactClick(child.title)"
              />
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
import { ListItem } from "@/types";
import GenericListItem from "@/components/common/generic/GenericListItem.vue";

/**
 * Displays the selected node's parents and children.
 */
export default Vue.extend({
  name: "ArtifactTraces",
  components: { GenericListItem },
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
    parents(): ListItem[] {
      if (!this.selectedArtifact) return [];

      return traceModule.traces
        .filter(({ sourceName }) => sourceName === this.selectedArtifact?.name)
        .map(({ targetName, targetId }) => ({
          title: targetName,
          subtitle: artifactModule.getArtifactById(targetId).type,
        }));
    },
    /**
     * @return The selected artifact's children.
     */
    children(): ListItem[] {
      if (!this.selectedArtifact) return [];

      return traceModule.traces
        .filter(({ targetName }) => targetName === this.selectedArtifact?.name)
        .map(({ sourceName, sourceId }) => ({
          title: sourceName,
          subtitle: artifactModule.getArtifactById(sourceId).type,
        }));
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
