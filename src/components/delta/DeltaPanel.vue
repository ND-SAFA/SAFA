<template>
  <v-container v-if="isOpen"> </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";

/**
 * Displays project version delta information.
 */
export default Vue.extend({
  name: "DeltaPanel",
  components: {},
  data() {
    return {};
  },
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "delta";
    },
  },
  methods: {},
});
</script>

<style scoped lang="scss"></style>
