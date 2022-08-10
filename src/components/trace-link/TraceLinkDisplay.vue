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

    <div class="d-flex flex-row justify-end">
      <v-btn
        outlined
        v-if="showApprove"
        color="primary"
        class="ma-1"
        @click="$emit('link:approve', link)"
      >
        Approve
      </v-btn>
      <v-btn
        outlined
        v-if="showDecline"
        color="error"
        class="ma-1"
        @click="$emit('link:decline', link)"
      >
        Decline
      </v-btn>
      <v-btn
        v-if="showDelete"
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
    </div>
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Artifact, TraceLink } from "@/types";
import { GenericArtifactBodyDisplay } from "@/components";
import { artifactModule } from "@/store";

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
    GenericArtifactBodyDisplay,
  },
  props: {
    link: {
      type: Object as PropType<TraceLink>,
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
    };
  },
  computed: {
    /**
     * @return The artifact this link comes from.
     */
    sourceArtifact(): Artifact {
      return artifactModule.getArtifactsById[this.link.sourceId];
    },
    /**
     * @return The artifact this link goes towards.
     */
    targetArtifact(): Artifact {
      return artifactModule.getArtifactsById[this.link.targetId];
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
     * Attempts to delete the link, after confirming.
     */
    handleDelete() {
      if (!this.confirmDelete) {
        this.confirmDelete = true;
      } else {
        this.$emit("link:delete", this.link);
      }
    },
  },
});
</script>
