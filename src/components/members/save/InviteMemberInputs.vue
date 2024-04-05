<template>
  <div class="long-input q-mx-auto">
    <typography variant="subtitle" value="Invite Members" />
    <separator b="2" />
    <typography secondary :value="subtitle" el="p" b="4" />
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
    <project-input
      v-if="props.entity.entityType === 'PROJECT'"
      v-model="entityIds"
      multiple
    />
    <multiselect-input
      v-else-if="props.entity.entityType === 'TEAM'"
      v-model="entityIds"
      label="Teams"
      option-value="id"
      option-label="name"
      option-to-value
      :options="teamStore.allTeams"
    />
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
import { computed, onMounted, ref, watch } from "vue";
import { InviteMemberInputsProps, MemberRole } from "@/types";
import { memberRoleOptions } from "@/util";
import { memberApiStore, teamStore } from "@/hooks";
import {
  ProjectInput,
  TextInput,
  SelectInput,
  TextButton,
  FlexBox,
  MultiselectInput,
  Typography,
  Separator,
} from "@/components/common";

const props = defineProps<InviteMemberInputsProps>();

const emit = defineEmits<{
  (e: "save"): void;
}>();

const roles = memberRoleOptions();

const entityIds = ref<string[]>([]);
const userEmail = ref("");
const userRole = ref<MemberRole>();

const subtitle = computed(
  () =>
    `Invite new members to this ${props.entity.entityType?.toLowerCase()}. Members must already have an account with SAFA.`
);

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
        id: "",
        email: userEmail.value,
        role: userRole.value,
        entityType: props.entity.entityType,
        entityId,
      },
      {
        onSuccess: () => emit("save"),
      }
    );
  });
}

/**
 * Resets the inputs to their default values.
 */
function handleReset() {
  entityIds.value = props.entity.entityId ? [props.entity.entityId] : [];
  userEmail.value = props.email || "";
  userRole.value = undefined;
}

onMounted(handleReset);

watch(
  () => [props.email, props.entity.entityId],
  () => handleReset()
);
</script>
