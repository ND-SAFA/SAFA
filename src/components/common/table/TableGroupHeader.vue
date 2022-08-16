<template>
  <td :colspan="data.headers.length">
    <flex-box y="2" x="2" align="center" justify="space-between">
      <flex-box align="center">
        <generic-icon-button
          small
          :icon-id="data.isOpen ? 'mdi-chevron-up' : 'mdi-chevron-down'"
          :tooltip="data.isOpen ? 'Hide Group' : 'Show Group'"
          @click="data.toggle"
        />
        <typography :value="displayGroupHeader(data.groupBy)" x="2" />
        <attribute-chip :value="data.group" :artifact-type="artifactType" />
        <typography secondary :value="String(data.items.length)" x="2" />
      </flex-box>
      <flex-box>
        <section-controls
          v-if="showExpand"
          @open:all="$emit('open:all', data)"
          @close:all="$emit('close:all', data)"
        />
        <generic-icon-button
          small
          icon-id="mdi-close"
          tooltip="Remove Grouping"
          @click="data.remove"
        />
      </flex-box>
    </flex-box>
  </td>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { DataTableGroup, FlatTraceLink } from "@/types";
import { camelcaseToDisplay } from "@/util";
import {
  FlexBox,
  AttributeChip,
  Typography,
  GenericIconButton,
} from "@/components/common";
import SectionControls from "./SectionControls.vue";

/**
 * Renders a group header in a table.
 *
 * @emits-1 `open:all` (DataTableGroup) - On open all expanded.
 * @emits-2 `close:all` (DataTableGroup) - On close all expanded.
 */
export default Vue.extend({
  name: "TableGroupHeader",
  components: {
    AttributeChip,
    GenericIconButton,
    Typography,
    FlexBox,
    SectionControls,
  },
  props: {
    data: Object as PropType<DataTableGroup>,
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
        this.data.groupBy.includes("type")
      );
    },
  },
  methods: {
    /**
     * Converts the group attributes into a display string.
     */
    displayGroupHeader(groupBy: (keyof FlatTraceLink)[]): string {
      return groupBy.map(camelcaseToDisplay).join(", ") + ":";
    },
  },
});
</script>

<style scoped></style>
