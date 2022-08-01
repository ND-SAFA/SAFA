<template>
  <private-page> </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { PrivatePage } from "@/components";

/**
 * Displays the account page.
 */
export default Vue.extend({
  name: "MyAccountView",
  components: {
    PrivatePage,
  },
});
</script>
