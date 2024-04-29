<template>
  <q-btn
    :color="props.color"
    :fab="props.fab"
    :disable="props.disabled"
    :size="size"
    :data-cy="props.dataCy"
    :flat="!props.fab"
    :round="!props.fab"
    @click="emit('click')"
  >
    <icon
      :id="props.iconId"
      :variant="props.icon"
      :rotate="props.rotate"
      :color="props.color"
    />
    <q-tooltip :delay="props.tooltipDelay || 200">
      {{ tooltip }}
    </q-tooltip>
    <slot />
  </q-btn>
</template>

<script lang="ts">
/**
 * A generic icon button.
 */
export default {
  name: "IconButton",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import type { IconButtonProps } from "@/types";
import { Icon } from "@/components/common/display";

const props = defineProps<IconButtonProps>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const size = computed(() => {
  if (props.small) {
    return "sm";
  } else if (props.large) {
    return "lg";
  } else {
    return "";
  }
});
</script>
