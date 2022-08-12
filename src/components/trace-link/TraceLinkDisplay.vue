<template>
  <div>
    <v-row class="my-1">
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

    <flex-box justify="end">
      <v-btn
        outlined
        v-if="showApprove"
        :loading="isApproveLoading"
        color="primary"
        class="ma-1"
        @click="handleApprove"
      >
        Approve
      </v-btn>
      <v-btn
        outlined
        v-if="showDecline"
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
        {{ deleteButtonText }}
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
import { ArtifactModel, TraceLinkModel } from "@/types";
import { GenericArtifactBodyDisplay } from "@/components";
import { artifactModule } from "@/store";
import { FlexBox } from "@/components/common";
import { handleApproveLink, handleDeclineLink } from "@/api";

/**
 * Displays a trace link.
 *
 * @emits-1 `link:approve` - On Link Approval.
 * @emits-2 `link:decline` - On Link Decline.
 * @emits-3 `link:delete` - On Link Delete.
 * @emits-4 `close` - On Close.
 */
export default Vue.extend({
  name: "TraceLinkDisplay",
  components: {
    FlexBox,
    GenericArtifactBodyDisplay,
  },
  props: {
    link: {
      type: Object as PropType<TraceLinkModel>,
      required: true,
    },
    showDecline: {
      type: Boolean,
      default: true,
    },
    showApprove: {
      type: Boolean,
      default: true,
    },
    showDelete: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      isSourceExpanded: false,
      isTargetExpanded: false,
      confirmDelete: false,
      isApproveLoading: false,
      isDeclineLoading: false,
      isDeleteLoading: false,
    };
  },
  computed: {
    /**
     * @return The artifact this link comes from.
     */
    sourceArtifact(): ArtifactModel {
      return artifactModule.getAllArtifactsById[this.link.sourceId];
    },
    /**
     * @return The artifact this link goes towards.
     */
    targetArtifact(): ArtifactModel {
      return artifactModule.getAllArtifactsById[this.link.targetId];
    },
    /**
     * @return The text to display on the delete button.
     */
    deleteButtonText(): string {
      return this.confirmDelete ? "Delete" : "Delete Link";
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
