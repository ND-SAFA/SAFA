<template>
  <panel-card class="full-width mr-2">
    <v-card-title>
      <typography el="h2" variant="subtitle" :value="project.name" />
    </v-card-title>
    <v-card-subtitle>
      <typography variant="caption" :value="version" />
    </v-card-subtitle>
    <v-card-text>
      <typography ep="p" :value="description" />
    </v-card-text>
    <v-card-actions>
      <div>
        <flex-box wrap b="4">
          <div class="mb-2">
            <attribute-chip
              :value="artifacts"
              icon="mdi-alpha-a-box-outline"
              color="primary"
            />
          </div>
          <div class="mb-2">
            <attribute-chip
              :value="traceLinks"
              icon="mdi-ray-start-arrow"
              color="primary"
            />
          </div>
        </flex-box>
        <flex-box
          wrap
          v-for="direction in typeDirections"
          :key="direction[0]"
          y="2"
          align="center"
        >
          <attribute-chip artifact-type :value="direction[0]" />
          <flex-box wrap>
            <v-icon class="mx-1">mdi-ray-start-arrow</v-icon>
            <div v-for="type in direction[1]" :key="type" class="mb-1">
              <attribute-chip artifact-type :value="type" />
            </div>
          </flex-box>
        </flex-box>
      </div>
    </v-card-actions>
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
    /**
     * @return The artifact type directions for this project.
     */
    typeDirections(): [string, string[]][] {
      return Object.entries(typeOptionsStore.artifactTypeDirections).filter(
        ([, targets]) => targets.length > 0
      );
    },
  },
});
</script>
