<template>
  <div>
    <text-input
      v-model="editedOrg.name"
      label="Organization Name"
      hint="Required"
      data-cy="input-org-name"
    />
    <text-input
      v-model="editedOrg.description"
      label="Organization Description"
      type="textarea"
      data-cy="input-org-description"
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
 * Inputs for editing an organization.
 */
export default {
  name: "SaveOrganizationInputs",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { appStore, orgApiStore, saveOrgStore } from "@/hooks";
import { FlexBox, TextButton, TextInput } from "@/components/common";

const editedOrg = computed(() => saveOrgStore.editedOrg);

const loading = computed(() => orgApiStore.saveOrgApiLoading);

/**
 * Saves the edited organization.
 */
function handleSave() {
  orgApiStore.handleSave(editedOrg.value, {
    onSuccess: () => appStore.close("saveOrg"),
  });
}
</script>
