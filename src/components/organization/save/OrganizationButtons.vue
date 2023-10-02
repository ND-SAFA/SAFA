<template>
  <flex-box t="2" class="settings-buttons">
    <q-btn-dropdown flat auto-close label="Switch Organizations">
      <flex-box column align="center" x="2" y="2">
        <text-button
          v-for="org in orgStore.unloadedOrgs"
          :key="org.id"
          text
          :label="org.name"
          @click="getOrgApiStore.handleSwitch(org)"
        />
        <text-button
          v-if="permissionStore.isAllowed('safa.create_orgs')"
          text
          color="primary"
          icon="add"
          label="Add Organization"
          @click="handleCreate(true)"
        />
      </flex-box>
    </q-btn-dropdown>
    <separator v-if="displayEdit" vertical />
    <text-button
      v-if="displayEdit"
      text
      label="Edit"
      icon="edit"
      data-cy="button-org-edit"
      @click="handleEdit"
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

    <modal
      size="sm"
      title="Create Organization"
      :open="createOpen"
      @close="handleCreate(false)"
    >
      <save-organization-inputs />
    </modal>
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
import { computed, ref } from "vue";
import {
  appStore,
  getOrgApiStore,
  orgApiStore,
  orgStore,
  permissionStore,
  saveOrgStore,
} from "@/hooks";
import { FlexBox, TextButton, Separator, Modal } from "@/components/common";
import { SaveOrganizationInputs } from "@/components/organization/save";

const createOpen = ref(false);

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

/**
 * Opens or closes the organization creator modal.
 */
function handleCreate(open?: boolean) {
  createOpen.value = open || false;
  saveOrgStore.resetOrg();
}
</script>
