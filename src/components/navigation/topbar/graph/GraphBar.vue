<template>
  <flex-box full-width justify="space-between" align="center">
    <flex-box align="center">
      <document-selector />
      <mode-buttons />
    </flex-box>
    <flex-box align="center">
      <graph-buttons />
      <v-divider inset vertical class="accent mx-1 mb-2 faded" />
      <commit-buttons />
    </flex-box>
  </flex-box>
</template>

<script lang="ts">
import Vue from "vue";
import { FlexBox, CommitButtons } from "@/components/common";
import { DocumentSelector } from "@/components/document";
import GraphButtons from "./GraphButtons.vue";
import ModeButtons from "./ModeButtons.vue";

/**
 * Renders options specific to the artifact graph.
 */
export default Vue.extend({
  name: "GraphBar",
  components: {
    ModeButtons,
    GraphButtons,
    CommitButtons,
    FlexBox,
    DocumentSelector,
  },
  props: {},
  data() {
    return {};
  },
  computed: {},
  methods: {},
});
</script>

<style scoped lang="scss"></style>
