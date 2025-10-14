<template>
  <div class="long-input q-mx-auto">
    <div v-if="!saveTeamStore.isUpdate">
      <typography variant="subtitle" value="Create Team" />
      <separator b="2" />
      <typography
        secondary
        value="
          Create a new team within this organization.
          Teams are used to group members and projects together
          with specific access permissions.
        "
        el="p"
        b="4"
      />
    </div>
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
import {
  FlexBox,
  Separator,
  TextButton,
  TextInput,
  Typography,
} from "@/components/common";

const emit = defineEmits<{
  (e: "submit"): void;
}>();

const editedTeam = computed(() => saveTeamStore.editedTeam);

const loading = computed(() => teamApiStore.saveTeamApiLoading);

/**
 * Saves the edited team.
 */
function handleSave() {
  teamApiStore.handleSave(editedTeam.value, {
    onSuccess: () => {
      appStore.close("saveTeam");
      emit("submit");
    },
  });
}
</script>
