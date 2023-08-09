<template>
  <modal :title="title" :open="props.open" size="md" @close="emit('close')">
    <text-input
      v-model="userEmail"
      label="Email"
      :error-message="emailErrorMessage"
      data-cy="input-settings-user-email"
    />
    <select-input
      v-model="userRole"
      label="Role"
      :options="projectRoles"
      option-label="name"
      option-value="id"
      option-to-value
      class="q-mb-lg"
      data-cy="input-settings-user-role"
    />
    <project-input v-if="!member" v-model="projectIds" multiple />
    <template #actions>
      <text-button
        :disabled="!isValid"
        :label="submitLabel"
        color="primary"
        data-cy="button-add-user-to-project"
        @click="handleSubmit"
      />
    </template>
  </modal>
</template>

<script lang="ts">
/**
 * ProjectMemberModal
 */
export default {
  name: "ProjectMemberModal",
};
</script>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { MembershipSchema, ProjectRole } from "@/types";
import { projectRoleOptions } from "@/util";
import { memberApiStore, projectStore } from "@/hooks";
import {
  Modal,
  ProjectInput,
  TextInput,
  SelectInput,
  TextButton,
} from "@/components/common";

const props = defineProps<{
  open: boolean;
  member?: MembershipSchema;
  email?: string | null;
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "submit"): void;
}>();

const projectRoles = projectRoleOptions();

const projectIds = ref<string[]>([]);
const userEmail = ref("");
const userRole = ref<ProjectRole>();

const isUpdate = computed(() => !!props.member);

const title = computed(() =>
  isUpdate.value ? "Edit Member" : "Share Project"
);

const submitLabel = computed(() =>
  isUpdate.value ? "Save" : "Add To Project"
);

const emailErrorMessage = computed(() => {
  if (
    userEmail.value &&
    !/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(userEmail.value)
  ) {
    return "E-mail must be valid";
  } else {
    return false;
  }
});

const isValid = computed(
  () =>
    userEmail.value.length > 0 &&
    !emailErrorMessage.value &&
    projectIds.value.length > 0 &&
    !!userRole.value
);

/**
 * Resets all modal data.
 */
function handleReset(): void {
  projectIds.value = [projectStore.projectId];
  userEmail.value = props.email || props.member?.email || "";
  userRole.value = props.member?.role;
}

/**
 * Adds or updates a project member.
 */
function handleSubmit() {
  projectIds.value.forEach((projectId) => {
    if (!isValid.value || !userRole.value) return;

    memberApiStore.handleInvite(projectId, userEmail.value, userRole.value, {
      onSuccess: () => emit("submit"),
    });
  });
}

watch(
  () => props.open,
  (open) => {
    if (!open) return;

    handleReset();
  }
);
</script>
