<template>
  <div v-if="open" class="q-py-sm">
    <slot />
  </div>
</template>

<script lang="ts">
/**
 * Controls the open state of a details right side panel.
 */
export default {
  name: "DetailsPanel",
};
</script>

<script setup lang="ts">
import { computed, watch } from "vue";
import { DetailsPanelProps } from "@/types";
import { appStore } from "@/hooks";

const props = defineProps<DetailsPanelProps>();

const emit = defineEmits<{
  (e: "open"): void;
}>();

const open = computed(() => appStore.popups.detailsPanel === props.panel);

watch(
  () => open.value,
  (open) => {
    if (!open) return;

    emit("open");
  }
);
</script>
