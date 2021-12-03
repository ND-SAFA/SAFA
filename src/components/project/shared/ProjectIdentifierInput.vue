<template>
  <v-container class="mb-0 pb-0" style="max-width: 30em">
    <v-text-field v-model="currentName" label="Project Name" required />
    <v-text-field
      v-model="currentDescription"
      label="Project description"
      required
    />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";

/**
 * Input fields for editing a project.
 *
 * @emits-1 `update:name` (string) - On name updated.
 * @emits-2 `update:description` (string) - On description updated.
 * @emits-3 `close` - On close.
 */
export default Vue.extend({
  props: {
    name: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
  },
  computed: {
    currentName: {
      get(): string {
        return this.name;
      },
      set(newName: string): void {
        this.$emit("update:name", newName);
      },
    },
    currentDescription: {
      get(): string {
        return this.description;
      },
      set(newDescription: string): void {
        this.$emit("update:description", newDescription);
      },
    },
  },
  methods: {
    clearData() {
      this.currentName = "";
      this.currentDescription = "";
    },
    onClose() {
      this.$emit("close");
      this.clearData();
    },
  },
});
</script>
