<template>
  <flex-box v-if="isOpen" full-width y="3">
    <v-text-field
      v-model="artifactName"
      filled
      required
      dense
      label="Artifact Type Name"
      :error-messages="errors"
      data-cy="input-artifact-type"
      @keydown.enter="handleEnterPress"
    />
    <v-btn
      :disabled="artifactName.length === 0"
      color="primary"
      class="ml-1 mt-2"
      data-cy="button-artifact-type"
      @click="handleSubmit"
    >
      Create Artifact Type
    </v-btn>
  </flex-box>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { FlexBox } from "@/components/common";

/**
 * Modal for creating new artifact types.
 *
 * @emits-1 `close` - On close.
 * @emits-2 `submit` (artifactName: string) - On submit.
 */
export default defineComponent({
  name: "ArtifactTypeCreator",
  components: { FlexBox },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    artifactTypes: {
      type: Array as PropType<string[]>,
      required: true,
    },
  },
  data() {
    return {
      artifactName: "",
      errors: [] as string[],
    };
  },
  watch: {
    /**
     * Empties the artifact name when opened.
     */
    isOpen(open: boolean): void {
      if (!open) return;

      this.artifactName = "";
    },
  },
  methods: {
    /**
     * Attempts to create a new artifact type panel.
     */
    handleSubmit() {
      if (this.artifactName === "")
        this.errors = ["Artifact type cannot be empty."];
      else if (this.artifactTypes.includes(this.artifactName))
        this.errors = [`Artifact type has already been created.`];
      else this.errors = [];
      if (this.errors.length === 0) {
        this.$emit("submit", this.artifactName);
        this.$emit("close");
      }
    },
    /**
     * Attempts to create a new artifact type panel when enter is pressed.
     */
    handleEnterPress(event: Event): void {
      event.preventDefault();
      this.handleSubmit();
    },
  },
});
</script>
