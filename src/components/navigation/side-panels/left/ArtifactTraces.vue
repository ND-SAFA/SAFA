<template>
  <div v-if="parents.length + children.length > 0" class="mb-2">
    <flex-box>
      <v-icon color="primary" style="transform: rotate(-45deg)">
        mdi-ray-start-arrow
      </v-icon>
      <typography el="h2" l="1" variant="subtitle" value="Trace Links" />
    </flex-box>

    <v-divider />

    <v-list expand>
      <toggle-list v-if="parents.length > 0" :title="parentTitle">
        <v-list dense style="max-height: 300px" class="overflow-y-auto">
          <template v-for="parent in parents">
            <generic-list-item
              :key="parent.title"
              :item="parent"
              @click="handleArtifactClick(parent.title)"
            />
          </template>
        </v-list>
      </toggle-list>
      <toggle-list v-if="children.length > 0" :title="childTitle">
        <v-list dense style="max-height: 300px" class="overflow-y-auto">
          <template v-for="child in children">
            <generic-list-item
              :key="child.title"
              :item="child"
              @click="handleArtifactClick(child.title)"
            />
          </template>
        </v-list>
      </toggle-list>
    </v-list>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { artifactModule, artifactSelectionModule, traceModule } from "@/store";
import { ListItem } from "@/types";
import {
  GenericListItem,
  Typography,
  FlexBox,
  ToggleList,
} from "@/components/common";

/**
 * Displays the selected node's parents and children.
 */
export default Vue.extend({
  name: "ArtifactTraces",
  components: { FlexBox, Typography, GenericListItem, ToggleList },
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
          subtitle: artifactModule.getArtifactById(targetId)?.type,
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
          subtitle: artifactModule.getArtifactById(sourceId)?.type,
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

      if (!artifact) return;

      artifactSelectionModule.selectArtifact(artifact.id);
    },
  },
});
</script>
