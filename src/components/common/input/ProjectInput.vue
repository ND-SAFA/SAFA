<template>
  <q-select
    :ref="projectInput"
    v-model="model"
    filled
    use-chips
    map-options
    emit-value
    :multiple="multiple"
    label="My Projects"
    :options="projects"
    option-label="name"
    option-value="projectId"
  />
</template>

<script lang="ts">
/**
 * An input for projects.
 */
export default {
  name: "ProjectInput",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { projectStore, useVModel } from "@/hooks";

const props = defineProps<{
  modelValue: string[] | string | undefined;
  multiple?: boolean;
  excludeCurrentProject?: boolean;
}>();

const projectInput = ref<HTMLElement | undefined>();

const model = useVModel(props, "modelValue");

const projects = computed(() =>
  props.excludeCurrentProject
    ? projectStore.unloadedProjects
    : projectStore.allProjects
);

/**
 * Closes the selection window.
 */
function handleClose(): void {
  projectInput.value?.blur();
}
</script>
