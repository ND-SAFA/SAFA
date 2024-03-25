<template>
  <modal
    :loading="projectApiStore.saveProjectLoading"
    :open="open"
    title="Transfer Project"
    subtitle="Move this project to another user, team, or organization."
    data-cy="modal-project-transfer"
    @close="handleClose"
  >
    <select-input
      v-model="ownerType"
      :options="options"
      label="Owner Type"
      option-value="id"
      option-label="name"
      option-to-value
      class="q-mb-md"
      data-cy="input-project-transfer-type"
    />
    <select-input
      v-if="ownerType === 'ORGANIZATION'"
      v-model="owner"
      :options="orgStore.allOrgs"
      label="New Project Owner"
      option-value="id"
      option-label="name"
      option-to-value
      class="q-mb-md"
      data-cy="input-project-transfer-org"
    />
    <select-input
      v-if="ownerType === 'TEAM'"
      v-model="owner"
      :options="teamStore.allTeams"
      label="New Project Owner"
      option-value="id"
      option-label="name"
      option-to-value
      class="q-mb-md"
      data-cy="input-project-transfer-team"
    />
    <select-input
      v-if="ownerType === 'USER_ID'"
      v-model="owner"
      :options="orgStore.org.members"
      label="New Project Owner"
      option-value="id"
      option-label="email"
      option-to-value
      class="q-mb-md"
      data-cy="input-project-transfer-member"
    />
    <text-input
      v-if="ownerType === 'USER_EMAIL'"
      v-model="owner"
      label="New Project Owner"
      data-cy="input-project-transfer-email"
    />
    <template #actions>
      <text-button
        color="primary"
        label="Transfer"
        :disabled="!canSubmit"
        :loading="projectApiStore.saveProjectLoading"
        data-cy="button-project-transfer"
        @click="handleConfirm"
      />
    </template>
  </modal>
</template>

<script lang="ts">
/**
 * A modal for confirming project deletion.
 */
export default {
  name: "TransferProjectModal",
};
</script>

<script setup lang="ts">
import { ref, computed } from "vue";
import { ProjectOwnerType } from "@/types";
import { ownerTypeOptions } from "@/util";
import { projectApiStore, appStore, orgStore, teamStore } from "@/hooks";
import { Modal, TextInput, TextButton, SelectInput } from "@/components/common";

const options = ownerTypeOptions();

const owner = ref("");
const ownerType = ref<ProjectOwnerType>("USER_EMAIL");

const open = computed(() => appStore.popups.moveProject);
const canSubmit = computed(() => !!owner.value);

/**
 * Clears the modal data and closes the modal.
 */
function handleClose(): void {
  owner.value = "";
  ownerType.value = "USER_EMAIL";
  appStore.close("moveProject");
}

/**
 * Confirms the project deletion.
 */
function handleConfirm(): void {
  projectApiStore.handleTransfer({
    owner: owner.value,
    ownerType: ownerType.value,
  });
}
</script>
