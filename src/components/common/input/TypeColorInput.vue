<template>
  <div class="overflow-hidden">
    <typography variant="caption" color="primary" value="Color" />
    <br />
    <q-btn-toggle
      v-model="color"
      flat
      style="flex-wrap: wrap"
      :options="colorOptions"
      :disable="!permissionStore.isAllowed('project.edit_data')"
      :toggle-color="currentColor"
      data-cy="button-type-options-color"
    />
  </div>
</template>

<script lang="ts">
/**
 * Renders an input for changing the color for an artifact type.
 */
export default {
  name: "TypeColorInput",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { ArtifactLevelInputProps } from "@/types";
import { ThemeGradient } from "@/util";
import { artifactTypeApiStore, permissionStore, timStore } from "@/hooks";
import { Typography } from "@/components/common/display";

const props = defineProps<ArtifactLevelInputProps>();

const currentColor = computed(() => props.artifactType.color);
const currentIcon = computed(() =>
  timStore.getTypeIcon(props.artifactType.name)
);

const colorOptions = computed(() =>
  Object.entries(ThemeGradient).map(([id, color]) => {
    const selected = currentColor.value === id;

    return {
      icon: currentIcon.value,
      label: "",
      value: id,
      text: !selected,
      outlined: selected,
      style: `color: ${color}`,
      class: selected ? "button-group-selected" : "",
    };
  })
);

const color = computed({
  get(): string {
    return props.artifactType.color;
  },
  set(color: string) {
    props.artifactType.color = color;

    artifactTypeApiStore.handleSave(props.artifactType);
  },
});
</script>
