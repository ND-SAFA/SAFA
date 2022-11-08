<template>
  <v-container v-if="isOpen"> </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";

/**
 * Allows for creating and editing artifacts.
 */
export default Vue.extend({
  name: "SaveArtifactPanel",
  components: {},
  data() {
    return {};
  },
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "saveArtifact";
    },
  },
  methods: {},
});
</script>

<style scoped lang="scss"></style>
