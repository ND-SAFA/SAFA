<template>
  <div class="long-input q-mx-auto">
    <text-input
      v-model="editedTeam.name"
      label="Team Name"
      hint="Required"
      data-cy="input-org-name"
    />
    <flex-box full-width justify="end">
      <text-button
        color="primary"
        label="Save"
        data-cy="button-org-save"
        :loading="loading"
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
import { computed } from "vue";
import { appStore, saveTeamStore, teamApiStore } from "@/hooks";
import { FlexBox, TextButton, TextInput } from "@/components/common";

const editedTeam = computed(() => saveTeamStore.editedTeam);

const loading = computed(() => teamApiStore.saveTeamApiLoading);

/**
 * Saves the edited team.
 */
function handleSave() {
  teamApiStore.handleSave(editedTeam.value, {
    onSuccess: () => appStore.close("saveTeam"),
  });
}
</script>
