<template>
  <div>
    <typography
      bold
      color="primary"
      class="q-mr-xs"
      :value="props.artifactType.name"
    />
    <typography secondary value="Traces To" />
    <div>
      <chip
        v-for="{ name } in allowedTypes"
        :key="name"
        outlined
        :removable="allowEditing"
        :label="getTypeLabel(name)"
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

const props = defineProps<ArtifactLevelInputProps>();

const allowEditing = computed(() =>
  sessionStore.isEditor(projectStore.project)
);

const allowedTypes = computed(() =>
  timStore.traceMatrices.filter(
    ({ sourceType }) => sourceType === props.artifactType.name
  )
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
