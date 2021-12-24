<template>
  <v-row v-if="isOpen" align="center" class="mx-auto my-3">
    <v-text-field
      v-model="artifactName"
      label="Artifact Name"
      required
      :error-messages="errors"
      @keydown.enter="onEnterPress"
    />
    <v-btn @click="onSubmit" color="primary" class="ml-1">
      Create Artifact
    </v-btn>
  </v-row>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

/**
 * Modal for creating new artifact types.
 *
 * @emits-1 `close` - On close.
 * @emits-2 `submit` (artifactName: string) - On submit.
 */
export default Vue.extend({
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
  methods: {
    onSubmit() {
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
    onEnterPress(event: Event): void {
      event.preventDefault();
      this.onSubmit();
    },
  },
  watch: {
    isOpen(isOpen: boolean): void {
      if (isOpen) {
        this.artifactName = "";
      }
    },
  },
});
</script>
