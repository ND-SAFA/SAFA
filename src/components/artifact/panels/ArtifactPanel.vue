<template>
  <v-container v-if="isOpen"> </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";

/**
 * Displays artifact information.
 */
export default Vue.extend({
  name: "ArtifactPanel",
  components: {},
  data() {
    return {};
  },
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "displayArtifact";
    },
  },
  methods: {},
});
</script>

<style scoped lang="scss"></style>
