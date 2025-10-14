<template>
  <div class="long-input q-mx-auto">
    <typography variant="subtitle" value="Invite Members" />
    <separator b="2" />
    <typography secondary :value="subtitle" el="p" b="4" />
    <email-input
      v-model="userEmail"
      v-model:error-message="emailErrorMessage"
      data-cy="input-member-email"
    />
    <select-input
      v-model="userRole"
      label="Role"
      hint="Required"
      :options="roles"
      :option-label="(opt: SelectOption) => `${opt.id}: ${opt.name}`"
      option-value="id"
      option-to-value
      class="q-mb-lg"
      data-cy="input-member-role"
    />
    <project-input
      v-if="props.entity.entityType === 'PROJECT'"
      v-model="entityIds"
      multiple
      hint="Required"
    />
    <multiselect-input
      v-else-if="props.entity.entityType === 'TEAM'"
      v-model="entityIds"
      label="Teams"
      option-value="id"
      option-label="name"
      option-to-value
      :options="teamStore.allTeams"
      hint="Required"
    />
    <flex-box full-width justify="between" t="2">
      <text-button
        :disabled="!isValidCopy"
        text
        label="Copy link"
        icon="link"
        data-cy="button-invite-link"
        @click="handleCopyLink"
      />
      <text-button
        :disabled="!isValidEmail"
        :label="submitLabel"
        color="primary"
        data-cy="button-invite-member"
        @click="handleSaveEmail"
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
import { InviteMemberInputsProps, MemberRole, SelectOption } from "@/types";
import { memberRoleOptions } from "@/util";
import { memberApiStore, teamStore } from "@/hooks";
import {
  ProjectInput,
  EmailInput,
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

const entityIds = ref<string[]>([]);
const userEmail = ref("");
const userRole = ref<MemberRole>();
const emailErrorMessage = ref<string | false>(false);

const roles = computed(() => memberRoleOptions(props.entity.entityType));

const subtitle = computed(
  () =>
    `Invite new members to this ${props.entity.entityType?.toLowerCase()}.
    Members will receive an email to accept the invite.`
);

const submitLabel = computed(
  () => `Invite to ${props.entity.entityType?.toLowerCase() || ""}`
);

const isValidCopy = computed(
  () => entityIds.value.length === 1 && !!userRole.value
);

const isValidEmail = computed(
  () =>
    userEmail.value.length > 0 &&
    !emailErrorMessage.value &&
    entityIds.value.length > 0 &&
    !!userRole.value
);

/**
 * Invites a member to the selected entities.
 */
function handleSaveEmail() {
  entityIds.value.forEach((entityId) => {
    if (!isValidEmail.value || !userRole.value) return;

    memberApiStore.handleInvite(
      {
        email: userEmail.value,
        role: userRole.value,
      },
      {
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
 * Creates a shareable link to the selected entities.
 */
function handleCopyLink() {
  if (!isValidCopy.value || !userRole.value) return;

  memberApiStore.handleInvite(
    { role: userRole.value },
    {
      entityType: props.entity.entityType,
      entityId: entityIds.value[0],
    }
  );
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
