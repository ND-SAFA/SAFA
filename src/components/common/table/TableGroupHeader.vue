<template>
  <td :colspan="data.headers.length" data-cy="artifact-table-group">
    <flex-box y="2" x="2" align="center" justify="space-between">
      <flex-box align="center">
        <icon-button
          small
          :icon-id="data.isOpen ? 'mdi-chevron-up' : 'mdi-chevron-down'"
          :tooltip="data.isOpen ? 'Hide Group' : 'Show Group'"
          @click="data.toggle"
        />
        <typography
          :value="groupHeader"
          x="2"
          data-cy="artifact-table-group-type"
        />
        <attribute-chip
          :value="data.group"
          :artifact-type="artifactType"
          :confidence-score="score"
          data-cy="artifact-table-group-value"
        />
        <attribute-chip
          v-if="displayArtifact"
          :value="headerType"
          artifact-type
        />
        <typography secondary :value="String(data.items.length)" x="2" />
      </flex-box>
      <flex-box>
        <section-controls
          v-if="showExpand"
          @open:all="$emit('open:all', data)"
          @close:all="$emit('close:all', data)"
        />
        <icon-button
          small
          icon-id="mdi-close"
          tooltip="Remove Grouping"
          @click="data.remove"
        />
      </flex-box>
    </flex-box>
    <div v-if="displayArtifact" class="mb-1">
      <typography
        default-expanded
        variant="expandable"
        :value="headerDescription"
      />
    </div>
  </td>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { DataTableGroup } from "@/types";
import { camelcaseToDisplay } from "@/util";
import { artifactStore } from "@/hooks";
import { IconButton } from "@/components/common/button";
import { FlexBox } from "@/components/common/layout";
import { AttributeChip, Typography } from "@/components/common/display";
import SectionControls from "./SectionControls.vue";

/**
 * Renders a group header in a table.
 *
 * @emits-1 `open:all` (DataTableGroup) - On open all expanded.
 * @emits-2 `close:all` (DataTableGroup) - On close all expanded.
 */
export default defineComponent({
  name: "TableGroupHeader",
  components: {
    AttributeChip,
    IconButton,
    Typography,
    FlexBox,
    SectionControls,
  },
  props: {
    data: {
      type: Object as PropType<DataTableGroup>,
      required: true,
    },
    showExpand: Boolean,
  },
  computed: {
    /**
     * @return Whether this group represents an artifact type.
     */
    artifactType(): boolean {
      return (
        this.data.groupBy.includes("sourceType") ||
        this.data.groupBy.includes("targetType") ||
        (this.data.groupBy as string[]).includes("type")
      );
    },
    /**
     * @return Whether this group represents a score.
     */
    score(): boolean {
      return this.data.groupBy.includes("score");
    },
    /**
     * @return The group attributes into a display string.
     */
    groupHeader(): string {
      return this.data.groupBy.map(camelcaseToDisplay).join(", ") + ":";
    },
    /**
     * @return Whether to render the description.
     */
    displayArtifact(): boolean {
      return (
        this.data.groupBy.includes("sourceName") ||
        this.data.groupBy.includes("targetName")
      );
    },
    /**
     * @return Renders artifact type when grouping by artifact.
     */
    headerDescription(): undefined | string {
      return this.displayArtifact
        ? artifactStore.getArtifactByName(this.data.group)?.body
        : undefined;
    },
    /**
     * @return Renders artifact type when grouping by artifact.
     */
    headerType(): undefined | string {
      return this.displayArtifact
        ? artifactStore.getArtifactByName(this.data.group)?.type
        : undefined;
    },
  },
});
</script>
