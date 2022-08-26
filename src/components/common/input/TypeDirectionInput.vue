<template>
  <div>
    <span class="mt-1">
      <typography bold color="primary" :value="entry.label" />
      <typography secondary value="Traces To" />
    </span>
    <v-chip-group column>
      <v-chip
        v-for="type in entry.allowedTypes"
        :key="type"
        close
        @click:close="handleDeleteDirection(entry, type)"
      >
        <typography :value="getTypeLabel(type)" />
      </v-chip>
    </v-chip-group>
    <v-chip v-if="entry.allowedTypes.length === 0">
      <typography value="Any Type" />
    </v-chip>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { LabelledTraceDirectionModel } from "@/types";
import { typeOptionsStore } from "@/hooks";
import { handleRemoveDirection } from "@/api";
import { Typography } from "@/components/common/display";

/**
 * Renders an input for changing the allowed artifact type directions.
 */
export default Vue.extend({
  name: "TypeDirectionInput",
  components: { Typography },
  props: {
    entry: Object as PropType<LabelledTraceDirectionModel>,
  },
  methods: {
    /**
     * Converts an artifact type to a title case name.
     * @param type - The type to convert.
     * @return The type display name.
     */
    getTypeLabel(type: string) {
      return typeOptionsStore.getArtifactTypeDisplay(type);
    },
    /**
     * Removes an artifact type direction.
     * @param entry - The type to update.
     * @param removedType - The type to remove.
     */
    handleDeleteDirection(
      entry: LabelledTraceDirectionModel,
      removedType: string
    ) {
      handleRemoveDirection(entry, removedType);
    },
  },
});
</script>
