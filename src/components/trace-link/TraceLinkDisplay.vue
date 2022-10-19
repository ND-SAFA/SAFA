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

    <flex-box
      full-width
      align="center"
      :justify="showScore ? 'space-between' : 'end'"
      v-if="!hideActions"
    >
      <flex-box align="center" v-if="showScore">
        <typography value="Confidence Score:" r="2" />
        <attribute-chip style="width: 200px" confidence-score :value="score" />
      </flex-box>

      <flex-box>
        <v-btn
          text
          v-if="showUnreviewed"
          :loading="isUnreviewLoading"
          class="ma-1"
          data-cy="button-trace-unreview"
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
          data-cy="button-trace-approve"
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
          data-cy="button-trace-decline"
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
          data-cy="button-trace-delete"
          @click="handleDelete"
        >
          {{ confirmDelete ? "Confirm Delete" : "Delete" }}
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
    </flex-box>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactModel, TraceLinkModel, TraceType } from "@/types";
import { linkStatus } from "@/util";
import { artifactStore, deltaStore, projectStore, sessionStore } from "@/hooks";
import {
  handleApproveLink,
  handleDeclineLink,
  handleUnreviewLink,
} from "@/api";
import { FlexBox, Typography, AttributeChip } from "@/components/common";
import { GenericArtifactBodyDisplay } from "@/components";

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
    AttributeChip,
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
     * @return Whether the current user is an editor of the current project.
     */
    isEditor(): boolean {
      return sessionStore.isEditor(projectStore.project);
    },
    /**
     * @return Whether this link can be modified.
     */
    canBeModified(): boolean {
      return (
        !this.hideActions &&
        this.link?.traceType === TraceType.GENERATED &&
        this.isEditor
      );
    },
    /**
     * @return Whether this link can be deleted.
     */
    showDelete(): boolean {
      return (
        linkStatus(this.link).canBeDeleted() &&
        !deltaStore.inDeltaView &&
        this.isEditor
      );
    },
    /**
     * @return Whether this link can be approved.
     */
    showApproved(): boolean {
      return !this.hideActions && linkStatus(this.link).canBeApproved();
    },
    /**
     * @return Whether this link can be declined.
     */
    showDeclined(): boolean {
      return !this.hideActions && linkStatus(this.link).canBeDeclined();
    },
    /**
     * @return Whether this link can be unreviewed.
     */
    showUnreviewed(): boolean {
      return !this.hideActions && linkStatus(this.link).canBeReset();
    },
    /**
     * @return The score of generated links.
     */
    score(): string {
      return this.canBeModified ? String(this.link.score) : "";
    },
    /**
     * @return Whether to display the score of generated links.
     */
    showScore(): boolean {
      return this.canBeModified ? !!this.score : false;
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
     * Attempts to delete the link, after confirming.
     */
    handleDelete() {
      if (!this.confirmDelete) {
        this.confirmDelete = true;
      } else {
        this.isDeleteLoading = true;
        handleDeclineLink(this.link, {
          onSuccess: () => this.$emit("link:delete", this.link),
          onComplete: () => (this.isDeleteLoading = false),
        });
      }
    },
  },
});
</script>
