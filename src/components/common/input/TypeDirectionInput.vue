<template>
  <div class="overflow-hidden">
    <typography
      bold
      ellipsis
      color="primary"
      class="q-mr-xs"
      :value="props.artifactLevel.name"
    />
    <typography secondary value="Traces To" />
    <div>
      <attribute-chip
        v-for="type in allowedTypes"
        :key="type"
        :value="getTypeLabel(type)"
        artifact-type
        :removable="allowEditing"
        data-cy="chip-type-direction"
        @remove="handleDelete(type)"
      />
      <chip v-if="allowedTypes.length === 0" outlined label="Any Type" />
    </div>
  </div>
</template>

<script lang="ts">
/**
 * Renders an input for changing the allowed artifact type directions.
 */
export default {
  name: "TypeDirectionInput",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { ArtifactLevelInputProps } from "@/types";
import {
  projectStore,
  sessionStore,
  traceMatrixApiStore,
  typeOptionsStore,
} from "@/hooks";
import { Typography, Chip } from "@/components/common/display";
import AttributeChip from "@/components/common/display/chip/AttributeChip.vue";

const props = defineProps<ArtifactLevelInputProps>();

const allowEditing = computed(() =>
  sessionStore.isEditor(projectStore.project)
);

const allowedTypes = computed(() => props.artifactLevel.allowedTypes);

/**
 * Converts an artifact type to a title case name.
 * @param type - The type to convert.
 * @return The type display name.
 */
function getTypeLabel(type: string) {
  return typeOptionsStore.getArtifactTypeDisplay(type);
}

/**
 * Removes an artifact type direction.
 * @param removedType - The type to remove.
 */
function handleDelete(removedType: string) {
  traceMatrixApiStore.handleDeleteDirection(props.artifactLevel, removedType);
}
</script>
