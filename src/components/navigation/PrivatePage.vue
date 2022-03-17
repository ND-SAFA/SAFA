<template>
  <v-container :class="fullWindow ? 'full-window-page' : ''">
    <slot name="page" />
    <app-bar :is-left-open="isLeftOpen" :is-right-open="isRightOpen" />
    <left-nav-drawer :is-left-open="isLeftOpen" :width="250" />
    <right-nav-drawer :is-right-open="isRightOpen" :width="325" />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { appModule } from "@/store";
import { LeftNavDrawer, RightNavDrawer } from "@/components/side-panels";
import AppBar from "./AppBar.vue";

export default Vue.extend({
  name: "private-page",
  components: {
    AppBar,
    LeftNavDrawer,
    RightNavDrawer,
  },
  props: {
    fullWindow: Boolean,
  },
  computed: {
    isLeftOpen: () => appModule.getIsLeftOpen,
    isRightOpen: () => appModule.getIsRightOpen,
  },
});
</script>
