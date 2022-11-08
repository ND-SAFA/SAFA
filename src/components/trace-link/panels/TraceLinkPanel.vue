<template>
  <v-container v-if="isOpen"> </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";

/**
 * Displays trace link information.
 */
export default Vue.extend({
  name: "TraceLinkPanel",
  components: {},
  data() {
    return {};
  },
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "displayTrace";
    },
  },
  methods: {},
});
</script>

<style scoped lang="scss"></style>
