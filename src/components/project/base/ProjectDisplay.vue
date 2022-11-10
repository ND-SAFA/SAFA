<template>
  <panel-card class="full-width mr-2">
    <flex-box align="center">
      <typography el="h2" variant="subtitle" :value="project.name" />
      <typography x="2" variant="caption" :value="version" />
    </flex-box>
    <v-divider class="mb-2" />
    <flex-box justify="space-between">
      <typography y="4" ep="p" :value="description" />
      <div>
        <flex-box justify="end">
          <attribute-chip
            :value="artifacts"
            icon="mdi-alpha-a-box-outline"
            color="primary"
          />
          <attribute-chip
            :value="traceLinks"
            icon="mdi-ray-start-arrow"
            color="primary"
          />
        </flex-box>
        <flex-box t="2" justify="end">
          <attribute-chip
            v-for="type in artifactTypes"
            :key="type"
            artifact-type
            :value="type"
          />
        </flex-box>
      </div>
    </flex-box>
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { versionToString } from "@/util";
import { projectStore, typeOptionsStore } from "@/hooks";
import {
  PanelCard,
  AttributeChip,
  Typography,
  FlexBox,
} from "@/components/common";

/**
 * ProjectDisplay.
 */
export default Vue.extend({
  name: "ProjectDisplay",
  components: { FlexBox, PanelCard, AttributeChip, Typography },
  computed: {
    /**
     * @return The current project.
     */
    project() {
      return projectStore.project;
    },
    /**
     * @return The version for this project.
     */
    version(): string {
      return `Version ${versionToString(this.project.projectVersion)}`;
    },
    /**
     * @return The artifact count for this project.
     */
    artifacts(): string {
      return `${this.project.artifacts.length} Artifacts`;
    },
    /**
     * @return The artifact count for this project.
     */
    traceLinks(): string {
      return `${this.project.traces.length} Trace Links`;
    },
    /**
     * @return The description for this project.
     */
    description(): string {
      return this.project.description || "No Description.";
    },
    /**
     * @return The artifact types for this project.
     */
    artifactTypes(): string[] {
      return typeOptionsStore.artifactTypes;
    },
  },
});
</script>
