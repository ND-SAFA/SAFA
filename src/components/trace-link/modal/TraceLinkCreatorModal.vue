<template>
  <generic-modal
    title="Create Trace Link"
    :is-open="isOpen"
    @close="$emit('close')"
    size="l"
  >
    <template v-slot:body>
      <v-row class="mt-2">
        <v-col cols="6">
          <artifact-input
            v-model="sourceArtifactId"
            label="Source Artifact"
            :multiple="false"
          />
        </v-col>
        <v-col cols="6">
          <artifact-input
            v-model="targetArtifactId"
            label="Target Artifact"
            :multiple="false"
          />
        </v-col>
      </v-row>
    </template>
    <template v-slot:actions>
      <v-spacer />
      <typography color="error" r="2" :value="errorMessage" />
      <v-btn color="primary" :disabled="!canSave" @click="handleSubmit">
        Create
      </v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue from "vue";
import { GenericModal, Typography, ArtifactInput } from "@/components/common";
import { artifactModule, traceModule } from "@/store";
import { handleCreateLink } from "@/api";
import { ArtifactModel } from "@/types";

/**
 * A modal for creating trace links.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "TraceLinkCreatorModal",
  components: { Typography, ArtifactInput, GenericModal },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      sourceArtifactId: "",
      targetArtifactId: "",
    };
  },
  watch: {
    isOpen(open: boolean) {
      if (!open) return;

      this.sourceArtifactId = "";
      this.targetArtifactId = "";
    },
  },
  computed: {
    /**
     * @return The source artifact.
     */
    sourceArtifact(): ArtifactModel {
      return artifactModule.getArtifactById(this.sourceArtifactId);
    },
    /**
     * @return The source artifact.
     */
    targetArtifact(): ArtifactModel {
      return artifactModule.getArtifactById(this.targetArtifactId);
    },
    /**
     * @return Any errors in trying to create this link.
     */
    errorMessage(): string {
      if (!this.sourceArtifactId || !this.targetArtifactId) return "";

      const isLinkAllowed = traceModule.isLinkAllowed(
        this.sourceArtifact,
        this.targetArtifact
      );

      return isLinkAllowed === true
        ? ""
        : isLinkAllowed || "Cannot create a trace link.";
    },
    /**
     * @return Whether a link can be created.
     */
    canSave(): boolean {
      return (
        !!this.sourceArtifactId &&
        !!this.targetArtifactId &&
        this.errorMessage === ""
      );
    },
  },
  methods: {
    /**
     * Creates a trace link from the given artifacts.
     */
    async handleSubmit(): Promise<void> {
      if (!this.sourceArtifactId || !this.targetArtifactId) return;

      await handleCreateLink(this.sourceArtifact, this.targetArtifact);

      this.$emit("close");
    },
  },
});
</script>
