<template>
  <v-avatar :size="size" @click.native="onAvatarClick">
    <img :src="pathToLogo" alt="SAFA" />
  </v-avatar>
</template>

<script lang="ts">
import Vue from "vue";
import { navigateTo, Routes } from "@/router";

export default Vue.extend({
  name: "safa-icon",
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
    onAvatarClick() {
      navigateTo(Routes.ARTIFACT);
    },
  },
});
</script>
