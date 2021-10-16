<template>
  <v-avatar :size="size" @click.native="onAvatarClick">
    <img :src="pathToLogo" alt="John" />
  </v-avatar>
</template>

<script lang="ts">
import Vue from "vue";
import router from "@/router";

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
      router.push("/");
    },
  },
});
</script>
