<template>
  <flex-box t="2" class="settings-buttons">
    <text-button
      v-if="displayEdit"
      text
      label="Edit"
      icon="edit"
      data-cy="button-org-edit"
      @click="handleEdit"
    />
    <text-button
      v-if="displayDelete"
      text
      label="Delete"
      icon="delete"
      data-cy="button-org-delete"
      :loading="orgApiStore.deleteOrgApiLoading"
      @click="orgApiStore.handleDelete"
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
import { computed } from "vue";
import {
  appStore,
  orgApiStore,
  orgStore,
  permissionStore,
  saveOrgStore,
} from "@/hooks";
import { FlexBox, TextButton } from "@/components/common";

const displayEdit = computed(() =>
  permissionStore.isAllowed("org.edit", orgStore.org)
);
const displayDelete = computed(() =>
  permissionStore.isAllowed("org.delete", orgStore.org)
);

/**
 * Opens the organization editor.
 */
function handleEdit() {
  saveOrgStore.resetOrg(orgStore.org);
  appStore.open("saveOrg");
}
</script>
