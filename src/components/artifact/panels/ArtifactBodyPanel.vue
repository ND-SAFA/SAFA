<template>
  <v-container v-if="isOpen"> </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";

/**
 * Displays artifact content.
 */
export default Vue.extend({
  name: "ArtifactBodyPanel",
  components: {},
  data() {
    return {};
  },
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "displayArtifactBody";
    },
  },
  methods: {},
});
</script>

<style scoped lang="scss"></style>
