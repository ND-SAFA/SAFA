<template>
  <div class="q-mx-auto long-input">
    <flex-box b="4">
      <select-input
        v-model="orgStore.org"
        label="Organization"
        :options="orgStore.allOrgs"
        class="q-mr-sm"
        option-to-value
        option-label="name"
        option-value="id"
      />
      <select-input
        v-model="teamStore.team"
        label="Team"
        :options="teamStore.allTeams"
        class="full-width"
        option-to-value
        option-label="name"
        option-value="id"
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
import { withDefaults } from "vue";
import { ProjectIdentifierProps } from "@/types";
import { orgStore, teamStore, useVModel } from "@/hooks";
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

//TODO: track org, team when creating projects using these inputs
//    - add to api store a current org, team that switching will load the new one.
//    - use these defaults for which org/team to create the current project under.
</script>
