<template>
  <q-linear-progress
    v-if="isLoading"
    rounded
    size="sm"
    indeterminate
    class="nav-gradient"
    data-cy="app-loading"
  />
</template>

<script lang="ts">
/**
 * Loading bar used in application header.
 */
export default {
  name: "LoadingBar",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { appStore } from "@/hooks";

const isLoading = computed(() => appStore.isLoading > 0);
</script>
