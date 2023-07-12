<template>
  <div>
    <typography
      bold
      color="primary"
      class="q-mr-xs"
      :value="props.artifactType.name"
    />
    <typography secondary value="Icon" />
    <q-btn-toggle
      v-model="icon"
      flat
      :options="iconOptions"
      :disable="!allowEditing"
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
import { allTypeIcons } from "@/util";
import { artifactTypeApiStore, projectStore, sessionStore } from "@/hooks";
import { Typography } from "@/components/common/display";

const props = defineProps<ArtifactLevelInputProps>();

const iconOptions = allTypeIcons.map((icon) => ({
  icon,
  label: "",
  value: icon,
}));

const allowEditing = computed(() =>
  sessionStore.isEditor(projectStore.project)
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
