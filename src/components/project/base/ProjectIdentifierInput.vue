<template>
  <div class="q-mx-auto" style="max-width: 40em">
    <text-input
      v-model="nameText"
      label="Project Name"
      hint="Required"
      :data-cy="props.dataCyName"
    />
    <text-input
      v-model="descriptionText"
      type="textarea"
      label="Project Description"
      :data-cy="props.dataCyDescription"
    />
  </div>
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
import { withDefaults } from "vue";
import { useVModel } from "@/hooks";
import { TextInput } from "@/components/common";

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

defineEmits<{
  (e: "update:name", name: string): void;
  (e: "update:description", description: string): void;
}>();

const nameText = useVModel(props, "name");
const descriptionText = useVModel(props, "description");
</script>
