<template>
  <div class="overflow-hidden">
    <typography variant="caption" color="primary" value="Icon" />
    <br />
    <q-btn-toggle
      v-model="icon"
      flat
      style="flex-wrap: wrap"
      :options="iconOptions"
      :disable="!permissionStore.isAllowed('project.edit_data')"
      :toggle-color="currentColor"
      data-cy="button-type-options-icon"
    />
  </div>
</template>

<script lang="ts">
/**
 * Renders an input for changing the icon for an artifact type.
 */
export default {
  name: "TypeIconInput",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { ArtifactLevelInputProps } from "@/types";
import { TypeIcons } from "@/util";
import { artifactTypeApiStore, permissionStore } from "@/hooks";
import { Typography } from "@/components/common/display";

const props = defineProps<ArtifactLevelInputProps>();

const currentColor = computed(() => props.artifactType.color);

const iconOptions = computed(() =>
  TypeIcons.map((icon) => {
    const selected = props.artifactType.icon === icon;

    return {
      icon,
      label: "",
      value: icon,
      text: !selected,
      outlined: selected,
      class: selected ? "button-group-selected" : "",
    };
  })
);

const icon = computed({
  get(): string {
    return props.artifactType.icon;
  },
  set(iconId: string) {
    props.artifactType.icon = iconId;

    artifactTypeApiStore.handleSave(props.artifactType);
  },
});
</script>
