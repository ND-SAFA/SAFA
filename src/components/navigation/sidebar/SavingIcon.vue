<template>
  <div v-if="isSaving">
    <div class="nav-saving-icon">
      <q-circular-progress color="secondary" indeterminate size="md" />
    </div>
    <icon color="secondary" variant="saving" size="sm" />
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
