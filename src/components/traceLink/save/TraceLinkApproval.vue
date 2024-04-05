<template>
  <flex-box
    v-if="displayActions"
    justify="between"
    align="center"
    class="width-max"
  >
    <flex-box align="center" justify="center">
      <icon-button
        v-if="showUnreview"
        tooltip="Un-Review"
        :loading="unreviewLoading"
        data-cy="button-trace-unreview"
        icon="trace-unreview"
        @click="handleUnreview"
      />
      <icon-button
        v-if="showApprove"
        tooltip="Approve"
        :loading="approveLoading"
        data-cy="button-trace-approve"
        icon="trace-approve"
        color="primary"
        @click="handleApprove"
      />
      <icon-button
        v-if="showDecline"
        tooltip="Decline"
        :loading="declineLoading"
        data-cy="button-trace-decline"
        icon="trace-decline"
        color="negative"
        @click="handleDecline"
      />
    </flex-box>
    <flex-box v-if="props.deletable">
      <separator v-if="showApprove || showDecline" vertical x="1" />
      <text-button
        text
        label="Edit"
        icon="edit"
        data-cy="button-trace-edit"
        @click="handleEdit"
      />
      <text-button
        text
        label="Delete"
        icon="delete"
        data-cy="button-trace-delete"
        @click="handleDelete"
      />
    </flex-box>
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays trace link approval buttons.
 */
export default {
  name: "TraceLinkApproval",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { TraceLinkApprovalProps } from "@/types";
import { linkStatus } from "@/util";
import { editTraceStore, permissionStore, traceApiStore } from "@/hooks";
import {
  FlexBox,
  TextButton,
  Separator,
  IconButton,
} from "@/components/common";

const props = defineProps<TraceLinkApprovalProps>();

const emit = defineEmits<{
  (e: "approve"): void;
  (e: "decline"): void;
  (e: "unreview"): void;
  (e: "delete"): void;
}>();

// Loading state is kept local to allow for multiple trace approval rows to display at once.
const approveLoading = ref(false);
const declineLoading = ref(false);
const unreviewLoading = ref(false);

const displayActions = computed(() =>
  permissionStore.isAllowed("project.edit_data")
);

const showApprove = computed(() => linkStatus(props.trace).canBeApproved());
const showDecline = computed(() => linkStatus(props.trace).canBeDeclined());
const showUnreview = computed(() => linkStatus(props.trace).canBeReset());

/**
 * Approves the given link and updates the stored links.
 */
function handleApprove() {
  approveLoading.value = true;
  traceApiStore.handleApprove(props.trace, {
    onSuccess: () => emit("approve"),
    onComplete: () => (approveLoading.value = false),
  });
}

/**
 * Declines the given link and updates the stored links.
 */
function handleDecline() {
  declineLoading.value = true;
  traceApiStore.handleDecline(props.trace, {
    onSuccess: () => emit("decline"),
    onComplete: () => (declineLoading.value = false),
  });
}

/**
 * Unreviews the given link and updates the stored links.
 */
function handleUnreview() {
  unreviewLoading.value = true;
  traceApiStore.handleUnreview(props.trace, {
    onSuccess: () => emit("unreview"),
    onComplete: () => (unreviewLoading.value = false),
  });
}

/**
 * Edits the given link.
 */
function handleEdit() {
  editTraceStore.openPanel(props.trace);
}

/**
 * Deletes the given link.
 */
function handleDelete() {
  traceApiStore.handleDelete(props.trace, {
    onSuccess: () => emit("delete"),
  });
}
</script>
