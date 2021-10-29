<template>
  <v-container class="mb-0 pb-0">
    <v-row>
      <v-text-field v-model="currentName" label="Project Name" required />
    </v-row>
    <v-row>
      <v-text-field
        v-model="currentDescription"
        label="Project description"
        required
      />
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";

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
  mounted() {
    this.clearData();
  },
  methods: {
    clearData() {
      this.currentName = "";
      this.currentDescription = "";
    },
    onClose() {
      this.$emit("onClose");
    },
  },
});
</script>
