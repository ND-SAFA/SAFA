<template>
  <q-separator
    :class="className"
    :vertical="props.vertical"
    :inset="props.inset"
    :color="separatorColor"
  />
</template>

<script lang="ts">
/**
 * A generic component for drawing a line separator.
 */
export default {
  name: "Separator",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { SeparatorProps } from "@/types";
import { useMargins } from "@/hooks";

const props = defineProps<SeparatorProps>();

const className = useMargins(props, () => [
  ["nav", "faded"],
  ["class", props.class],
]);

const separatorColor = computed(() => {
  if (props.color) {
    return props.color;
  } else if (props.nav) {
    return "text";
  } else {
    return undefined;
  }
});
</script>
