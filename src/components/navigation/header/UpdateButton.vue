<template>
  <v-btn v-if="hasUpdate" outlined small color="secondary" @click="handleClick">
    <v-icon class="mr-1">mdi-reload</v-icon>
    Load Project Updates
  </v-btn>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";

/**
 * Renders a button to update the current project.
 */
export default Vue.extend({
  name: "UpdateButton",
  computed: {
    /**
     * @return Whether the app has an update.
     */
    hasUpdate(): boolean {
      return !!appStore.runUpdate;
    },
  },
  methods: {
    /**
     * Runs the current update.
     */
    async handleClick(): Promise<void> {
      await appStore.loadAppChanges();
    },
  },
});
</script>
