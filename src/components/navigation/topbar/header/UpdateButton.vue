<template>
  <text-button
    v-if="hasUpdate"
    text
    small
    color="accent"
    icon-id="mdi-cloud-sync-outline"
    data-cy="button-nav-load-update"
    @click="handleClick"
  >
    Load Project Updates
  </text-button>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";
import { TextButton } from "@/components/common";

/**
 * Renders a button to update the current project.
 */
export default Vue.extend({
  name: "UpdateButton",
  components: { TextButton },
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
