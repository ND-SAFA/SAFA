<template>
  <div>
    <panel-card>
      <artifact-body-display
        :artifact="targetArtifact"
        display-title
        display-divider
        data-cy="panel-trace-link-target"
      />
      <v-card-actions>
        <text-button
          text
          data-cy="button-trace-target"
          variant="artifact"
          @click="handleViewTarget"
        >
          View Artifact
        </text-button>
      </v-card-actions>
    </panel-card>
    <flex-box justify="center" b="4">
      <v-icon large style="transform: rotate(270deg)">
        mdi-ray-start-arrow
      </v-icon>
      <attribute-chip
        v-if="!!score"
        style="width: 200px"
        confidence-score
        :value="score"
      />
    </flex-box>
    <panel-card>
      <artifact-body-display
        :artifact="sourceArtifact"
        display-title
        display-divider
        data-cy="panel-trace-link-source"
      />
      <v-card-actions>
        <v-btn text data-cy="button-trace-source" @click="handleViewSource">
          <v-icon class="mr-1">mdi-application-array-outline</v-icon>
          View Artifact
        </v-btn>
      </v-card-actions>
    </panel-card>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { ArtifactSchema, TraceLinkSchema, TraceType } from "@/types";
import { artifactStore, selectionStore } from "@/hooks";
import {
  ArtifactBodyDisplay,
  FlexBox,
  AttributeChip,
  PanelCard,
  TextButton,
} from "@/components/common";

/**
 * Displays trace link information.
 */
export default defineComponent({
  name: "TraceLinkContent",
  components: {
    TextButton,
    PanelCard,
    FlexBox,
    ArtifactBodyDisplay,
    AttributeChip,
  },
  computed: {
    /**
     * @return The selected trace link.
     */
    traceLink(): TraceLinkSchema | undefined {
      return selectionStore.selectedTraceLink;
    },
    /**
     * @return The artifact this link comes from.
     */
    sourceArtifact(): ArtifactSchema | undefined {
      return artifactStore.getArtifactById(this.traceLink?.sourceId || "");
    },
    /**
     * @return The artifact this link goes towards.
     */
    targetArtifact(): ArtifactSchema | undefined {
      return artifactStore.getArtifactById(this.traceLink?.targetId || "");
    },
    /**
     * @return The score of generated links.
     */
    score(): string {
      return this.traceLink?.traceType === TraceType.GENERATED
        ? String(this.traceLink.score)
        : "";
    },
  },
  methods: {
    /**
     * Views the target artifact.
     */
    handleViewTarget(): void {
      selectionStore.selectArtifact(this.traceLink?.targetId || "");
    },
    /**
     * Views the source artifact.
     */
    handleViewSource(): void {
      selectionStore.selectArtifact(this.traceLink?.sourceId || "");
    },
  },
});
</script>

<style scoped lang="scss"></style>
