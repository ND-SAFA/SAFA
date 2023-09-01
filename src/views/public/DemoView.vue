<template>
  <card-page id="login-view">
    <template #form>
      <typography value="Loading demo account..." />
    </template>
  </card-page>
</template>

<script lang="ts">
/**
 * Displays the login page.
 */
export default {
  name: "LoginView",
};
</script>

<script setup lang="ts">
import { onMounted } from "vue";
import { sessionApiStore } from "@/hooks";
import { CardPage, Typography } from "@/components";

onMounted(() => {
  sessionApiStore.handleDemoLogin();
});
</script>
