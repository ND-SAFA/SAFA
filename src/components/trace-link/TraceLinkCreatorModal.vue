<template>
  <generic-modal
    title="Trace Link"
    :is-open="isOpen"
    @close="$emit('close')"
    size="l"
  >
    <template v-slot:body>
      <v-row class="mt-8">
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
      <v-row justify="end">
        <v-btn color="primary" :disabled="!canSave" @click="handleSubmit">
          Create
        </v-btn>
      </v-row>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue from "vue";
import { GenericModal } from "@/components/common";
import ArtifactInput from "@/components/common/input/ArtifactInput.vue";
import { artifactModule, traceModule } from "@/store";
import { handleCreateLink } from "@/api";
import { Artifact } from "@/types";

/**
 * A modal for creating trace links.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "TraceLinkCreatorModal",
  components: { ArtifactInput, GenericModal },
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
    sourceArtifact(): Artifact {
      return artifactModule.getArtifactById(this.sourceArtifactId);
    },
    /**
     * @return The source artifact.
     */
    targetArtifact(): Artifact {
      return artifactModule.getArtifactById(this.targetArtifactId);
    },
    /**
     * @return Whether a link can be created.
     */
    canSave(): boolean {
      return (
        !!this.sourceArtifactId &&
        !!this.targetArtifactId &&
        traceModule.isLinkAllowed(this.sourceArtifact, this.targetArtifact)
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
