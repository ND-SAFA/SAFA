<template>
  <q-select
    v-model="orgApiStore.currentOrg"
    standout
    bg-color="transparent"
    class="nav-breadcrumb"
    label="Organization"
    :options="orgStore.allOrgs"
    option-value="id"
    option-label="name"
  >
    <template #after-options>
      <text-button
        v-if="permissionStore.isAllowed('safa.create_orgs')"
        text
        color="primary"
        icon="add"
        label="Add Organization"
        @click="handleCreate(true)"
      />
      <modal
        size="sm"
        title="Create Organization"
        :open="createOpen"
        @close="handleCreate(false)"
      >
        <save-organization-inputs />
      </modal>
    </template>
  </q-select>
</template>

<script lang="ts">
/**
 * Displays an organization's actions.
 */
export default {
  name: "OrganizationSelector",
};
</script>

<script setup lang="ts">
import { ref } from "vue";
import { orgApiStore, orgStore, permissionStore, saveOrgStore } from "@/hooks";
import { Modal, TextButton } from "@/components/common";
import { SaveOrganizationInputs } from "@/components/organization/save";

const createOpen = ref(false);

/**
 * Opens or closes the organization creator modal.
 */
function handleCreate(open?: boolean) {
  createOpen.value = open || false;
  saveOrgStore.resetOrg();
}
</script>
