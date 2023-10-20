<template>
  <private-page small-window>
    <my-account />
  </private-page>
</template>

<script lang="ts">
/**
 * Displays the account page.
 */
export default {
  name: "MyAccountView",
};
</script>

<script setup lang="ts">
import { PrivatePage, MyAccount } from "@/components";
</script>
