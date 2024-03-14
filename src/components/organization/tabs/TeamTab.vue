<template>
  <panel-card title="Teams" :subtitle="subtitle">
    <template #title-actions>
      <text-button
        v-if="addMode"
        text
        label="Cancel"
        icon="cancel"
        @click="handleClose"
      />
    </template>

    <selector-table
      v-if="!addMode"
      v-model:selected="selectedTeams"
      addable
      deletable
      :columns="teamColumns"
      :rows="teamStore.allTeams"
      :loading="loading"
      row-key="id"
      item-name="team"
      @row:add="addMode = true"
      @row:delete="teamApiStore.handleDelete"
    >
      <template #cell-actions="{ row }">
        <icon-button
          v-if="displayLeave(row)"
          icon="leave"
          tooltip="Leave team"
          data-cy="button-selector-leave"
          @click="handleLeave(row)"
        />
      </template>
    </selector-table>
    <save-team-inputs v-else @submit="addMode = false" />
  </panel-card>
</template>

<script lang="ts">
/**
 * A tab for managing teams within an organization.
 */
export default {
  name: "TeamTab",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { TeamSchema } from "@/types";
import { teamColumns } from "@/util";
import { memberApiStore, sessionStore, teamApiStore, teamStore } from "@/hooks";
import { navigateTo, QueryParams, Routes } from "@/router";
import {
  PanelCard,
  TextButton,
  IconButton,
  SelectorTable,
} from "@/components/common";
import { SaveTeamInputs } from "@/components/organization/save";

const selectedTeam = ref<TeamSchema>();

const loading = ref(false);
const addMode = ref(false);

const selectedTeams = computed({
  get() {
    return selectedTeam.value ? [selectedTeam.value] : [];
  },
  set(teams: TeamSchema[]) {
    selectedTeam.value = teams[0];

    if (teams[0]) {
      teamApiStore.handleSwitch(teams[0], {
        onSuccess: () =>
          navigateTo(Routes.TEAM, {
            [QueryParams.TEAM]: teams[0].id,
          }),
      });
    }
  },
});

const subtitle = computed(() =>
  addMode.value ? "Create a new team." : "Manage teams and permissions."
);

/**
 * Closes the add team form and resets entered data.
 */
function handleClose() {
  addMode.value = false;
}

/**
 * Whether to display the leave button for a team.
 */
function displayLeave(team: TeamSchema): boolean {
  const member = team.members.find(
    ({ email }) => email === sessionStore.userEmail
  );

  return !!member && team.members.length > 1;
}

/**
 * Leaves the selected team.
 */
function handleLeave(team: TeamSchema) {
  const member = team.members.find(
    ({ email }) => email === sessionStore.userEmail
  );

  if (!member) return;

  memberApiStore.handleDelete(member);
}
</script>
