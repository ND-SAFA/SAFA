<template>
  <flex-box t="2" class="settings-buttons">
    <q-btn-dropdown flat auto-close label="Switch Teams">
      <flex-box column align="center">
        <text-button text label="Other Team 1" />
        <text-button text label="Other Team 2" />
        <text-button text color="primary" icon="add" label="Add Team" />
      </flex-box>
    </q-btn-dropdown>
    <separator vertical />
    <text-button
      text
      label="Edit"
      icon="edit"
      data-cy="button-team-edit"
      @click="appStore.openPanel(PanelType.teamEditor)"
    />
    <separator vertical />
    <text-button
      text
      label="Delete"
      icon="delete"
      data-cy="button-team-delete"
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
import { PanelType } from "@/types";
import { appStore } from "@/hooks";
import { FlexBox, TextButton, Separator } from "@/components/common";
</script>
