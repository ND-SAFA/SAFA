<template>
  <div v-if="isSaving">
    <q-circular-progress color="primary" indeterminate size="md" />
    <icon color="primary" variant="saving" class="nav-saving-icon" />
    <q-tooltip> Saving... </q-tooltip>
  </div>
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
