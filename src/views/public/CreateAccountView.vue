<template>
  <card-page> </card-page>
</template>

<script lang="ts">
import Vue from "vue";
import { CardPage } from "@/components";

/**
 * Presents the create account page.
 */
export default Vue.extend({
  name: "create-account-view",
  components: { CardPage },
});
</script>
