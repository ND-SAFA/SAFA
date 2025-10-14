<template>
  <div v-if="open" class="q-pb-sm">
    <flex-box justify="between" align="center" b="2">
      <icon-button
        icon="cancel"
        tooltip="Close panel"
        data-cy="button-close-details"
        class="float-left"
        @click="selectionStore.clearSelections()"
      />
      <flex-box>
        <slot name="actions" />
      </flex-box>
    </flex-box>
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
import { appStore, selectionStore } from "@/hooks";
import FlexBox from "@/components/common/display/content/FlexBox.vue";
import { IconButton } from "@/components";

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
