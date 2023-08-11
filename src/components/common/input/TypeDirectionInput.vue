<template>
  <div class="overflow-hidden">
    <typography variant="caption" color="primary" value="Parent Types" />
    <div>
      <attribute-chip
        v-for="name in allowedTypes"
        :key="name"
        :value="getTypeLabel(name)"
        artifact-type
        :removable="allowEditing"
        data-cy="chip-type-direction"
        @remove="handleDelete(name)"
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
  timStore,
  traceMatrixApiStore,
} from "@/hooks";
import { Typography, Chip } from "@/components/common/display";
import AttributeChip from "@/components/common/display/chip/AttributeChip.vue";

const props = defineProps<ArtifactLevelInputProps>();

const allowEditing = computed(() =>
  sessionStore.isEditor(projectStore.project)
);

const allowedTypes = computed(() =>
  timStore.traceMatrices
    .filter(({ sourceType }) => sourceType === props.artifactType.name)
    .map(({ targetType }) => targetType)
);

/**
 * Converts an artifact type to a title case name.
 * @param type - The type to convert.
 * @return The type display name.
 */
function getTypeLabel(type: string) {
  return timStore.getTypeName(type);
}

/**
 * Removes an artifact type direction.
 * @param removedType - The type name to remove.
 */
function handleDelete(removedType: string) {
  traceMatrixApiStore.handleDeleteTypes(props.artifactType.name, removedType);
}
</script>
