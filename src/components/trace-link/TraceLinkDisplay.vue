<template>
  <div>
    <v-row class="my-1" v-if="!showOnly">
      <v-col cols="6">
        <generic-artifact-body-display
          :artifact="sourceArtifact"
          display-title
          display-divider
        />
      </v-col>

      <v-divider vertical inset />

      <v-col cols="6">
        <generic-artifact-body-display
          :artifact="targetArtifact"
          display-title
          display-divider
        />
      </v-col>
    </v-row>

    <typography
      v-else
      defaultExpanded
      secondary
      t="1"
      variant="expandable"
      :value="showOnly === 'source' ? sourceArtifact.body : targetArtifact.body"
    />

    <flex-box justify="end">
      <v-btn
        text
        v-if="showUnreviewed"
        :loading="isUnreviewLoading"
        class="ma-1"
        @click="handleUnreview"
      >
        Unreview
      </v-btn>
      <v-btn
        outlined
        v-if="showApproved"
        :loading="isApproveLoading"
        color="primary"
        class="ma-1"
        @click="handleApprove"
      >
        Approve
      </v-btn>
      <v-btn
        outlined
        v-if="showDeclined"
        :loading="isDeclineLoading"
        color="error"
        class="ma-1"
        @click="handleDecline"
      >
        Decline
      </v-btn>
      <v-btn
        v-if="showDelete"
        :loading="isDeleteLoading"
        color="error"
        class="ma-1"
        :text="!confirmDelete"
        :outlined="confirmDelete"
        @click="handleDelete"
      >
        Delete
      </v-btn>
      <v-btn
        outlined
        v-if="confirmDelete"
        @click="confirmDelete = false"
        class="ma-1"
      >
        Cancel
      </v-btn>
    </flex-box>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import {
  ApprovalType,
  ArtifactModel,
  TraceLinkModel,
  TraceType,
} from "@/types";
import { GenericArtifactBodyDisplay } from "@/components";
import { artifactStore, deltaStore } from "@/hooks";
import { FlexBox } from "@/components/common";
import {
  handleApproveLink,
  handleDeclineLink,
  handleUnreviewLink,
} from "@/api";
import Typography from "@/components/common/display/Typography.vue";

/**
 * Displays a trace link.
 *
 * @emits-1 `link:approve` - On Link Approval.
 * @emits-2 `link:decline` - On Link Decline.
 * @emits-2 `link:unreview` - On Link Unreview.
 * @emits-3 `link:delete` - On Link Delete.
 * @emits-4 `close` - On Close.
 */
export default Vue.extend({
  name: "TraceLinkDisplay",
  components: {
    Typography,
    FlexBox,
    GenericArtifactBodyDisplay,
  },
  props: {
    link: {
      type: Object as PropType<TraceLinkModel>,
      required: true,
    },
    hideActions: Boolean,
    showOnly: String as PropType<"source" | "target">,
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
     * @return The artifact this link comes from.
     */
    sourceArtifact(): ArtifactModel | undefined {
      return artifactStore.getArtifactById(this.link.sourceId);
    },
    /**
     * @return The artifact this link goes towards.
     */
    targetArtifact(): ArtifactModel | undefined {
      return artifactStore.getArtifactById(this.link.targetId);
    },
    /**
     * @return Whether this link can be modified.
     */
    canBeModified(): boolean {
      return !this.hideActions && this.link?.traceType === TraceType.GENERATED;
    },
    /**
     * @return Whether this link can be deleted.
     */
    showDelete(): boolean {
      return (
        !this.canBeModified && !this.hideActions && !deltaStore.inDeltaView
      );
    },
    /**
     * @return Whether this link can be approved.
     */
    showApproved(): boolean {
      return (
        this.canBeModified && this.link.approvalStatus !== ApprovalType.APPROVED
      );
    },
    /**
     * @return Whether this link can be declined.
     */
    showDeclined(): boolean {
      return (
        this.canBeModified && this.link.approvalStatus !== ApprovalType.DECLINED
      );
    },
    /**
     * @return Whether this link can be unreviewed.
     */
    showUnreviewed(): boolean {
      return (
        this.canBeModified &&
        this.link.approvalStatus !== ApprovalType.UNREVIEWED
      );
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
    /**
     * Attempts to delete the link, after confirming.
     */
    handleDelete() {
      if (!this.confirmDelete) {
        this.confirmDelete = true;
      } else {
        this.isDeleteLoading = true;
        handleDeclineLink(this.link, {
          onSuccess: () => {
            this.isDeleteLoading = false;
            this.$emit("link:delete", this.link);
          },
          onError: () => (this.isDeleteLoading = false),
        });
      }
    },
  },
});
</script>
