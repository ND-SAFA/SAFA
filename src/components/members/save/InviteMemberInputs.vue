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
      :options="roles"
      :option-label="(opt) => `${opt.id}: ${opt.name}`"
      option-value="id"
      option-to-value
      class="q-mb-lg"
      data-cy="input-member-role"
    />
    <project-input v-model="entityIds" multiple />
    <flex-box full-width justify="end" t="2">
      <text-button
        :disabled="!isValid"
        :label="submitLabel"
        color="primary"
        data-cy="button-invite-member"
        @click="handleSave"
      />
    </flex-box>
  </div>
</template>

<script lang="ts">
/**
 * Inputs for inviting a new member to a project, team, or organization.
 */
export default {
  name: "InviteMemberInputs",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { InviteMemberInputsProps, MemberRole } from "@/types";
import { memberRoleOptions } from "@/util";
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

const roles = memberRoleOptions();

const entityIds = ref<string[]>([]);
const userEmail = ref("");
const userRole = ref<MemberRole>();

const submitLabel = computed(
  () => `Invite to ${props.entity.entityType?.toLowerCase() || ""}`
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
    entityIds.value.length > 0 &&
    !!userRole.value
);

/**
 * Invites a member to the selected projects.
 */
function handleSave() {
  entityIds.value.forEach((entityId) => {
    if (!isValid.value || !userRole.value) return;

    memberApiStore.handleInvite(
      {
        projectMembershipId: "",
        email: userEmail.value,
        role: userRole.value,
        entityType: "PROJECT",
        entityId,
      },
      {
        onSuccess: () => emit("save"),
      }
    );
  });
}

onMounted(() => {
  entityIds.value = props.entity.entityId ? [props.entity.entityId] : [];
  userEmail.value = props.email || "";
});
</script>
