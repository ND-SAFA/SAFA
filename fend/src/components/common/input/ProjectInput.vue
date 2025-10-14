<template>
  <q-select
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
import { computed } from "vue";
import { ProjectInputProps } from "@/types";
import { projectStore, useVModel } from "@/hooks";

const props = defineProps<ProjectInputProps>();

const model = useVModel(props, "modelValue");

const projects = computed(() =>
  props.excludeCurrentProject
    ? projectStore.unloadedProjects
    : projectStore.allProjects
);
</script>
