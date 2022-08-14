<template>
  <td :colspan="data.headers.length">
    <flex-box y="2" x="2" align="center">
      <generic-icon-button
        small
        icon-id="mdi-close"
        tooltip="Remove Grouping"
        @click="data.remove"
      />
      <generic-icon-button
        small
        :icon-id="data.isOpen ? 'mdi-chevron-up' : 'mdi-chevron-down'"
        :tooltip="data.isOpen ? 'Hide Group' : 'Show Group'"
        @click="data.toggle"
      />
      <typography :value="displayGroupHeader(data.groupBy)" x="2" />
      <attribute-chip :value="data.group" :artifact-type="artifactType" />
      <typography secondary :value="data.items.length" x="2" />
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

/**
 * Renders a group header in the trace link table.
 */
export default Vue.extend({
  name: "TraceLinkTableGroup",
  components: {
    AttributeChip,
    GenericIconButton,
    Typography,
    FlexBox,
  },
  props: {
    data: Object as PropType<DataTableGroup<FlatTraceLink>>,
  },
  computed: {
    /**
     * @return Whether this group represents an artifact type.
     */
    artifactType(): boolean {
      return (
        this.data.groupBy.includes("sourceType") ||
        this.data.groupBy.includes("targetType")
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
