<template>
  <div class="full-width">
    <flex-box full-width justify="space-between">
      <flex-box align="center">
        <searchbar v-if="graphVisible" />
      </flex-box>
      <flex-box align="center">
        <update-button />
        <saving-icon />
        <app-version />
      </flex-box>
    </flex-box>
    <v-divider class="accent faded mt-2" v-if="graphVisible" />
    <loading-bar />
  </div>
</template>

<script lang="ts">
import Vue, { ref, watch } from "vue";
import { useRoute } from "vue-router";
import { Routes } from "@/router";
import { FlexBox } from "@/components/common";
import Searchbar from "./Searchbar.vue";
import AppVersion from "./AppVersion.vue";
import SavingIcon from "./SavingIcon.vue";
import UpdateButton from "./UpdateButton.vue";
import LoadingBar from "./LoadingBar.vue";

/**
 * Renders the top navigation bar header.
 */
export default Vue.extend({
  name: "HeaderBar",
  components: {
    Searchbar,
    SavingIcon,
    UpdateButton,
    AppVersion,
    FlexBox,
    LoadingBar,
  },
  setup() {
    const currentRoute = useRoute();
    const graphVisible = ref(currentRoute.path === Routes.ARTIFACT);

    watch(
      () => currentRoute.path,
      () => (graphVisible.value = currentRoute.path === Routes.ARTIFACT)
    );

    return { graphVisible };
  },
});
</script>
