<template>
  <v-container style="max-width: 40em">
    <v-text-field
      v-model="name"
      filled
      label="Project Name"
      :data-cy="dataCyName"
      hint="Required"
      persistent-hint
    />
    <v-textarea
      v-model="description"
      filled
      hide-details
      label="Project Description"
      rows="3"
      :data-cy="dataCyDescription"
    />
  </v-container>
</template>

<script lang="ts">
/**
 * Input fields for editing a project.
 */
export default {
  name: "ProjectIdentifierInput",
};
</script>

<script setup lang="ts">
import { withDefaults, defineProps, defineEmits } from "vue";
import { useVModel } from "@/hooks";

const props = withDefaults(
  defineProps<{
    name: string;
    description: string;
    dataCyName?: string;
    dataCyDescription?: string;
  }>(),
  {
    dataCyName: "input-project-name",
    dataCyDescription: "input-project-description",
  }
);

const emit = defineEmits<{
  (e: "update:name", name: string): void;
  (e: "update:description", description: string): void;
}>();

const name = useVModel(props, "name");
const description = useVModel(props, "description");
</script>
