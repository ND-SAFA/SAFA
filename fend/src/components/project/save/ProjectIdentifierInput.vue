<template>
  <div class="q-mx-auto long-input">
    <flex-box v-if="!props.isUpdate" b="4">
      <select-input
        v-model="orgApiStore.currentOrg"
        label="Organization"
        :options="orgStore.allOrgs"
        class="q-mr-sm"
        option-label="name"
      />
      <select-input
        v-model="teamApiStore.currentTeam"
        label="Team"
        :options="teamStore.teamsWithCreateProject"
        class="full-width"
        option-label="name"
      />
    </flex-box>
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
import { ProjectIdentifierProps } from "@/types";
import {
  orgApiStore,
  orgStore,
  teamApiStore,
  teamStore,
  useVModel,
} from "@/hooks";
import { FlexBox, SelectInput, TextInput } from "@/components/common";

const props = withDefaults(defineProps<ProjectIdentifierProps>(), {
  dataCyName: "input-project-name",
  dataCyDescription: "input-project-description",
});

defineEmits<{
  (e: "update:name", name: string): void;
  (e: "update:description", description: string): void;
}>();

const nameText = useVModel(props, "name");
const descriptionText = useVModel(props, "description");
</script>
