<template>
  <q-list :bordered="props.bordered">
    <div
      v-if="!!props.scrollHeight"
      class="scrollable"
      :style="`max-height: ${props.scrollHeight}px`"
    >
      <slot />
    </div>
    <slot v-else />
  </q-list>
</template>

<script lang="ts">
/**
 * A generic list component.
 */
export default {
  name: "List",
};
</script>

<script setup lang="ts">
import { ListProps } from "@/types";

const props = defineProps<ListProps>();
</script>
