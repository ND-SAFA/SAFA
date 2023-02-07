<template>
  <v-chip
    v-if="doDisplay"
    outlined
    :color="isGenerated ? 'secondary' : 'primary'"
    @click.stop="handleClick"
  >
    <typography :value="source.name" />
    <v-icon class="mx-1" :style="arrowStyle">mdi-ray-start-arrow</v-icon>
    <typography :value="target.name" />
  </v-chip>
  <div v-else class="show-on-hover">
    <div @click.stop class="width-fit">
      <icon-button
        icon-id="mdi-plus"
        tooltip="Create trace link"
        @click="handleCreateLink"
      />
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { FlatArtifact, TraceLinkSchema, TraceType } from "@/types";
import { appStore, selectionStore, traceStore } from "@/hooks";
import { Typography, IconButton } from "@/components/common";

/**
 * Renders a chip representing a trace link between two artifacts.
 */
export default Vue.extend({
  name: "TraceMatrixChip",
  components: {
    IconButton,
    Typography,
  },
  props: {
    source: {
      type: Object as PropType<FlatArtifact>,
      required: true,
    },
    target: {
      type: Object as PropType<FlatArtifact>,
      required: true,
    },
  },
  computed: {
    /**
     * @return The relationship from the parent to the child artifact.
     */
    relationship(): "Parent" | "Child" | string {
      return this.source[this.target.id];
    },
    /**
     * @return Whether the relationship is as a child.
     */
    isChild(): boolean {
      return this.relationship === "Child";
    },
    /**
     * @return Whether to display the chip.
     */
    doDisplay(): boolean {
      return !!this.relationship;
    },
    /**
     * @return The style for the chip arrow.
     */
    arrowStyle(): string {
      return this.isChild ? "transform: rotate(-180deg)" : "";
    },
    /**
     * @return The trace link between these artifacts.
     */
    traceLink(): TraceLinkSchema | undefined {
      return this.isChild
        ? traceStore.getTraceLinkByArtifacts(this.target.id, this.source.id)
        : traceStore.getTraceLinkByArtifacts(this.source.id, this.target.id);
    },
    /**
     * @return Whether this trace link is generated
     */
    isGenerated(): boolean {
      return this.traceLink?.traceType === TraceType.GENERATED;
    },
  },
  methods: {
    /**
     * Selects the trace link represented by this chip.
     */
    handleClick(): void {
      const traceLink = this.traceLink;

      if (!traceLink) return;

      selectionStore.selectTraceLink(traceLink);
    },
    /**
     * Opens the trace creation panel to create a link between these artifacts.
     */
    handleCreateLink(): void {
      appStore.openTraceCreatorTo({
        type: "both",
        sourceId: this.source.id,
        targetId: this.target.id,
      });
    },
  },
});
</script>
