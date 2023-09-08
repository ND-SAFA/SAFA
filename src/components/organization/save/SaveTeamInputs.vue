<template>
  <div class="long-input q-mx-auto">
    <text-input
      v-model="name"
      label="Team Name"
      hint="Required"
      data-cy="input-org-name"
    />
    <flex-box full-width justify="end">
      <text-button
        color="primary"
        label="Save"
        data-cy="button-org-save"
        @click="handleSave"
      />
    </flex-box>
  </div>
</template>

<script lang="ts">
/**
 * Inputs for creating a team.
 */
export default {
  name: "SaveTeamInputs",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { teamApiStore, teamStore } from "@/hooks";
import { FlexBox, TextButton, TextInput } from "@/components/common";

const team = computed(() => teamStore.team);

const name = ref(team.value.name);

/**
 * Saves the edited organization.
 */
function handleSave() {
  teamApiStore.handleEdit({
    ...team.value,
    name: name.value,
  });
}
</script>
