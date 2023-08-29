<template>
  <flex-box t="2" class="settings-buttons">
    <q-btn-dropdown flat auto-close label="Switch Organizations">
      <flex-box column align="center">
        <text-button text label="Other Org 1" />
        <text-button text label="Other Org 2" />
        <text-button text color="primary" icon="add" label="Add Organization" />
      </flex-box>
    </q-btn-dropdown>
    <separator vertical />
    <text-button text label="Edit" icon="edit" data-cy="button-org-edit" />
    <separator vertical />
    <text-button
      text
      label="Delete"
      icon="delete"
      data-cy="button-org-delete"
    />
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays an organization's actions.
 */
export default {
  name: "OrganizationButtons",
};
</script>

<script setup lang="ts">
import { FlexBox, TextButton, Separator } from "@/components/common";
</script>
