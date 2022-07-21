<template>
  <v-avatar :size="size" @click.native="onAvatarClick">
    <img :src="pathToLogo" alt="SAFA" />
  </v-avatar>
</template>

<script lang="ts">
import Vue from "vue";
import { navigateTo, Routes } from "@/router";

/**
 * Displays the SAFA icon.
 */
export default Vue.extend({
  name: "SafaIcon",
  props: {
    size: {
      type: Number,
      required: false,
      default: 50,
    },
  },
  data() {
    return {
      pathToLogo: require("@/assets/SAFA.png"),
    };
  },
  methods: {
    /**
     * Navigates to the project creator when the logo is clicked.
     */
    onAvatarClick() {
      navigateTo(Routes.HOME);
    },
  },
});
</script>
