<template>
  <div class="long-input q-mx-auto">
    <text-input
      v-model="userEmail"
      label="Email"
      :error-message="emailErrorMessage"
      data-cy="input-member-email"
    />
    <select-input
      v-model="userRole"
      label="Role"
      :options="projectRoles"
      :option-label="(opt) => `${opt.id}: ${opt.name}`"
      option-value="id"
      option-to-value
      class="q-mb-lg"
      data-cy="input-member-role"
    />
    <project-input v-model="projectIds" multiple />
    <flex-box full-width justify="end" t="2">
      <text-button
        :disabled="!isValid"
        label="Invite member"
        color="primary"
        data-cy="button-invite-member"
        @click="handleSave"
      />
    </flex-box>
  </div>
</template>

<script lang="ts">
/**
 * Inputs for inviting a new project member.
 */
export default {
  name: "InviteMemberInputs",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { InviteMemberInputsProps, ProjectRole } from "@/types";
import { projectRoleOptions } from "@/util";
import { memberApiStore } from "@/hooks";
import {
  ProjectInput,
  TextInput,
  SelectInput,
  TextButton,
  FlexBox,
} from "@/components/common";

const props = defineProps<InviteMemberInputsProps>();

const emit = defineEmits<{
  (e: "save"): void;
}>();

const projectRoles = projectRoleOptions();

const projectIds = ref<string[]>([]);
const userEmail = ref("");
const userRole = ref<ProjectRole>();

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
 * Invites a member to the selected projects.
 */
function handleSave() {
  projectIds.value.forEach((projectId) => {
    if (!isValid.value || !userRole.value) return;

    memberApiStore.handleInvite(projectId, userEmail.value, userRole.value, {
      onSuccess: () => emit("save"),
    });
  });
}

onMounted(() => {
  projectIds.value = props.projectId ? [props.projectId] : [];
  userEmail.value = props.email || "";
});
</script>
