<template>
  <div>
    <typography
      bold
      color="primary"
      class="q-mr-xs"
      :value="props.artifactLevel.name"
    />
    <typography secondary value="Traces To" />
    <div>
      <q-chip
        v-for="type in allowedTypes"
        :key="type"
        outline
        :removable="allowEditing"
        data-cy="chip-type-direction"
        @close="handleDelete(type)"
      >
        <typography :value="getTypeLabel(type)" />
      </q-chip>
      <q-chip v-if="allowedTypes.length === 0">
        <typography value="Any Type" />
      </q-chip>
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
import { TimArtifactLevelSchema } from "@/types";
import { projectStore, sessionStore, typeOptionsStore } from "@/hooks";
import { handleRemoveDirection } from "@/api";
import { Typography } from "@/components/common/display";

const props = defineProps<{
  /**
   * The artifact level to display and allow editing of.
   */
  artifactLevel: TimArtifactLevelSchema;
}>();

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
  handleRemoveDirection(props.artifactLevel, removedType);
}
</script>
