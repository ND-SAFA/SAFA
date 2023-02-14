<template>
  <flex-box v-if="doDisplay" justify="space-between">
    <flex-box align="center" justify="center">
      <text-button
        v-if="showUnreviewed"
        text
        :loading="isUnreviewLoading"
        data-cy="button-trace-unreview"
        icon-id="mdi-checkbox-blank-circle-outline"
        @click="handleUnreview"
      >
        Un-Review
      </text-button>
      <text-button
        v-if="showApproved"
        text
        :loading="isApproveLoading"
        color="primary"
        data-cy="button-trace-approve"
        icon-id="mdi-check-circle-outline"
        @click="handleApprove"
      >
        Approve
      </text-button>
      <text-button
        v-if="showDeclined"
        text
        :loading="isDeclineLoading"
        color="error"
        data-cy="button-trace-decline"
        icon-id="mdi-close-circle-outline"
        @click="handleDecline"
      >
        Decline
      </text-button>
    </flex-box>
    <flex-box v-if="showDelete">
      <v-divider v-if="showApproved || showDeclined" vertical />
      <text-button
        text
        variant="delete"
        data-cy="button-trace-delete"
        @click="handleDelete"
      >
        Delete
      </text-button>
    </flex-box>
  </flex-box>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { TraceLinkSchema } from "@/types";
import { linkStatus } from "@/util";
import { projectStore, sessionStore } from "@/hooks";
import {
  handleApproveLink,
  handleDeclineLink,
  handleDeleteLink,
  handleUnreviewLink,
} from "@/api";
import { FlexBox, TextButton } from "@/components/common";

/**
 * Displays trace link approval buttons.
 *
 * @emits-1 `link:approve` - On Link Approval.
 * @emits-2 `link:decline` - On Link Decline.
 * @emits-2 `link:unreview` - On Link Un-review.
 * @emits-2 `link:delete` - On Link Delete.
 */
export default defineComponent({
  name: "TraceLinkApproval",
  components: {
    TextButton,
    FlexBox,
  },
  props: {
    link: {
      type: Object as PropType<TraceLinkSchema>,
      required: true,
    },
    showDelete: Boolean,
  },
  data() {
    return {
      isApproveLoading: false,
      isDeclineLoading: false,
      isUnreviewLoading: false,
    };
  },
  computed: {
    /**
     * @return Whether to display these buttons.
     */
    doDisplay(): boolean {
      return sessionStore.isEditor(projectStore.project);
    },
    /**
     * @return Whether this link can be approved.
     */
    showApproved(): boolean {
      return linkStatus(this.link).canBeApproved();
    },
    /**
     * @return Whether this link can be declined.
     */
    showDeclined(): boolean {
      return linkStatus(this.link).canBeDeclined();
    },
    /**
     * @return Whether this link can be unreviewed.
     */
    showUnreviewed(): boolean {
      return linkStatus(this.link).canBeReset();
    },
  },
  methods: {
    /**
     * Approves the given link and updates the stored links.
     */
    handleApprove() {
      this.isApproveLoading = true;
      handleApproveLink(this.link, {
        onSuccess: () => this.$emit("link:approve", this.link),
        onComplete: () => (this.isApproveLoading = false),
      });
    },
    /**
     * Declines the given link and updates the stored links.
     */
    handleDecline() {
      this.isDeclineLoading = true;
      handleDeclineLink(this.link, {
        onSuccess: () => this.$emit("link:decline", this.link),
        onComplete: () => (this.isDeclineLoading = false),
      });
    },
    /**
     * Unreviews the given link and updates the stored links.
     */
    handleUnreview() {
      this.isDeclineLoading = true;
      handleUnreviewLink(this.link, {
        onSuccess: () => this.$emit("link:unreview", this.link),
        onComplete: () => (this.isDeclineLoading = false),
      });
    },
    /**
     * Deletes the given link.
     */
    handleDelete() {
      handleDeleteLink(this.link, {
        onSuccess: () => this.$emit("link:delete", this.link),
      });
    },
  },
});
</script>
