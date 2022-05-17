<template>
  <v-container>
    <v-row>
      <v-col cols="6">
        <h1 class="text-h5">{{ link.sourceName }}</h1>
        <v-divider />
        <generic-artifact-body-display :body="sourceBody" />
      </v-col>

      <v-divider vertical inset />

      <v-col cols="6">
        <h1 class="text-h5">{{ link.targetName }}</h1>
        <v-divider />
        <generic-artifact-body-display :body="targetBody" />
      </v-col>
    </v-row>

    <div class="d-flex flex-row justify-end pt-5">
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
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TraceLink } from "@/types";
import { GenericArtifactBodyDisplay } from "@/components";

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
    sourceBody: {
      type: String,
      required: true,
    },
    targetBody: {
      type: String,
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
