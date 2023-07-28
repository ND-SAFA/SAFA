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
import { navigateTo, QueryParams, Routes } from "@/router";
import { CardPage, Typography } from "@/components";

onMounted(() => {
  sessionApiStore
    .handleLogin({
      email: "view@safa.ai",
      password: "safa!",
    })
    .then(() =>
      navigateTo(Routes.ARTIFACT, {
        [QueryParams.VERSION]: "c59b3a2c-56eb-4290-a37b-9c8f36deffd0",
      })
    );
});
</script>
