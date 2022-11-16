<template>
  <private-page>
    <template v-slot:page>
      <my-account />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { PrivatePage, MyAccount } from "@/components";

/**
 * Displays the account page.
 */
export default Vue.extend({
  name: "MyAccountView",
  components: {
    MyAccount,
    PrivatePage,
  },
});
</script>
