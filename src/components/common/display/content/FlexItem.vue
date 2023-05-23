<template>
  <div :class="className">
    <slot />
  </div>
</template>

<script lang="ts">
/**
 * A generic flex box child.
 */
export default {
  name: "FlexItem",
};
</script>

<script setup lang="ts">
import { FlexItemProps } from "@/types";
import { useMargins } from "@/hooks";

const props = defineProps<FlexItemProps>();

const className = useMargins(props, () => [
  ["parts", `col-${props.parts}`],
  ["fullWidth", "full-width"],
]);
</script>
