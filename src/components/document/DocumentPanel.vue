<template>
  <v-container v-if="isOpen"> </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";

/**
 * Allows for creating and editing documents.
 */
export default Vue.extend({
  name: "DocumentPanel",
  components: {},
  data() {
    return {};
  },
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "document";
    },
  },
  methods: {},
});
</script>

<style scoped lang="scss"></style>
