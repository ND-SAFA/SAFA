<template>
  <modal
    title="Share Project"
    :open="props.open"
    size="md"
    @close="emit('close')"
  >
    <invite-member-inputs
      v-if="props.open"
      :project-id="props.projectId"
      :email="props.email"
      @save="emit('submit')"
    />
  </modal>
</template>

<script lang="ts">
/**
 * A modal for inviting project members.
 */
export default {
  name: "InviteMemberModal",
};
</script>

<script setup lang="ts">
import { ProjectMemberModalProps } from "@/types";
import { Modal } from "@/components/common";
import InviteMemberInputs from "./InviteMemberInputs.vue";

const props = defineProps<ProjectMemberModalProps>();

const emit = defineEmits<{
  (e: "close"): void;
  (e: "submit"): void;
}>();
</script>
