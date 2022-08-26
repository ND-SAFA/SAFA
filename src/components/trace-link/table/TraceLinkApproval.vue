<template>
  <flex-box align="center" justify="center">
    <generic-icon-button
      v-if="showUnreviewed"
      :loading="isUnreviewLoading"
      icon-id="mdi-checkbox-blank-circle-outline"
      tooltip="Unreview"
      @click="handleUnreview"
    />
    <generic-icon-button
      v-if="showApproved"
      :loading="isApproveLoading"
      color="primary"
      icon-id="mdi-check-circle-outline"
      tooltip="Approve"
      @click="handleApprove"
    />
    <generic-icon-button
      v-if="showDeclined"
      :loading="isDeclineLoading"
      color="error"
      icon-id="mdi-close-circle-outline"
      tooltip="Decline"
      @click="handleDecline"
    />
  </flex-box>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TraceLinkModel } from "@/types";
import { linkStatus } from "@/util";
import {
  handleApproveLink,
  handleDeclineLink,
  handleUnreviewLink,
} from "@/api";
import { FlexBox, GenericIconButton } from "@/components/common";

/**
 * Displays trace link approval buttons.
 *
 * @emits-1 `link:approve` - On Link Approval.
 * @emits-2 `link:decline` - On Link Decline.
 * @emits-2 `link:unreview` - On Link Un-review.
 */
export default Vue.extend({
  name: "TraceLinkApproval",
  components: {
    GenericIconButton,
    FlexBox,
  },
  props: {
    link: {
      type: Object as PropType<TraceLinkModel>,
      required: true,
    },
  },
  data() {
    return {
      isSourceExpanded: false,
      isTargetExpanded: false,
      confirmDelete: false,
      isApproveLoading: false,
      isDeclineLoading: false,
      isUnreviewLoading: false,
      isDeleteLoading: false,
    };
  },
  computed: {
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
        onSuccess: () => {
          this.isApproveLoading = false;
          this.$emit("link:approve", this.link);
        },
        onError: () => (this.isApproveLoading = false),
      });
    },
    /**
     * Declines the given link and updates the stored links.
     */
    handleDecline() {
      this.isDeclineLoading = true;
      handleDeclineLink(this.link, {
        onSuccess: () => {
          this.isDeclineLoading = false;
          this.$emit("link:decline", this.link);
        },
        onError: () => (this.isDeclineLoading = false),
      });
    },
    /**
     * Unreviews the given link and updates the stored links.
     */
    handleUnreview() {
      this.isDeclineLoading = true;
      handleUnreviewLink(this.link, {
        onSuccess: () => {
          this.isDeclineLoading = false;
          this.$emit("link:unreview", this.link);
        },
        onError: () => (this.isDeclineLoading = false),
      });
    },
  },
});
</script>
