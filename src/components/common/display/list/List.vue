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
const props = defineProps<{
  /**
   * Whether to add a border to the list.
   */
  bordered?: boolean;
  /**
   * The number of pixels to set the scroll area height to.
   */
  scrollHeight?: number;
}>();
</script>
