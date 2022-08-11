<template>
  <v-container style="max-width: 30em">
    <v-text-field
      outlined
      v-model="currentName"
      label="Project Name"
      data-cy="input-project-name"
    />
    <v-textarea
      outlined
      hide-details
      v-model="currentDescription"
      label="Project Description"
      rows="3"
      data-cy="input-project-description"
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
  name: "ProjectIdentifierInput",
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
    /**
     * Emits changes to the name.
     */
    currentName: {
      get(): string {
        return this.name;
      },
      set(newName: string): void {
        this.$emit("update:name", newName);
      },
    },
    /**
     * Emits changes to the description.
     */
    currentDescription: {
      get(): string {
        return this.description;
      },
      set(newDescription: string): void {
        this.$emit("update:description", newDescription);
      },
    },
  },
});
</script>
