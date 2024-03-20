<template>
  <flex-box t="2" class="settings-buttons">
    <q-btn-dropdown flat auto-close label="Switch Teams">
      <flex-box column align="center" x="2" y="2">
        <text-button
          v-for="t in orgStore.org.teams"
          :key="t.id"
          text
          :label="t.name"
          @click="teamApiStore.currentTeam = t"
        />
      </flex-box>
    </q-btn-dropdown>
    <separator v-if="displayEdit" vertical />
    <text-button
      v-if="displayEdit"
      text
      label="Edit"
      icon="edit"
      data-cy="button-team-edit"
      @click="handleEdit"
    />
    <separator v-if="displayDelete" vertical />
    <text-button
      v-if="displayDelete"
      text
      label="Delete"
      icon="delete"
      data-cy="button-team-delete"
      @click="teamApiStore.handleDelete(team)"
    />
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays a team's actions.
 */
export default {
  name: "TeamButtons",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import {
  appStore,
  orgStore,
  permissionStore,
  saveTeamStore,
  teamApiStore,
  teamStore,
} from "@/hooks";
import { FlexBox, TextButton, Separator } from "@/components/common";

const team = computed(() => teamStore.team);

const displayEdit = computed(() =>
  permissionStore.isAllowed("team.edit", teamStore.team)
);
const displayDelete = computed(() =>
  permissionStore.isAllowed("team.delete", teamStore.team)
);

/**
 * Opens the team editor.
 */
function handleEdit() {
  saveTeamStore.resetTeam(team.value);
  appStore.open("saveTeam");
}
</script>
