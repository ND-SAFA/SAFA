<template>
  <flex-box t="2" class="settings-buttons">
    <q-btn-dropdown flat auto-close label="Switch Organizations">
      <flex-box column align="center">
        <text-button
          v-for="org in getOrgApiStore.unloadedOrgs"
          :key="org.id"
          text
          :label="org.name"
          @click="getOrgApiStore.handleSwitch(org)"
        />
        <!--        <text-button-->
        <!--          text-->
        <!--          color="primary"-->
        <!--          icon="add"-->
        <!--          label="Add Organization"-->
        <!--          @click="orgApiStore.handleCreate"-->
        <!--        />-->
      </flex-box>
    </q-btn-dropdown>
    <separator v-if="displayEdit" vertical />
    <text-button
      v-if="displayEdit"
      text
      label="Edit"
      icon="edit"
      data-cy="button-org-edit"
      @click="appStore.open('saveOrg')"
    />
    <separator v-if="displayDelete" vertical />
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
  getOrgApiStore,
  orgApiStore,
  orgStore,
  permissionStore,
} from "@/hooks";
import { FlexBox, TextButton, Separator } from "@/components/common";

const displayEdit = computed(() =>
  permissionStore.isAllowed("org.edit", orgStore.org)
);
const displayDelete = computed(() =>
  permissionStore.isAllowed("org.delete", orgStore.org)
);
</script>
