<template>
  <v-tooltip v-if="isSaving" bottom z-index="10000">
    <template #activator="{ props }">
      <v-progress-circular
        v-bind="props"
        indeterminate
        size="36"
        color="accent"
      >
        <icon color="accent" variant="saving" />
      </v-progress-circular>
    </template>
    <span>Saving...</span>
  </v-tooltip>
</template>

<script lang="ts">
/**
 * Renders app saving state.
 */
export default {
  name: "SavingIcon",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { appStore } from "@/hooks";
import { Icon } from "@/components/common";

const isSaving = computed(() => appStore.isSaving);
</script>
