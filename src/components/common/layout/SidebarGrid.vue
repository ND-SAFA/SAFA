<template>
  <div>
    <slot name="header" />
    <flex-box :column="smallWindow">
      <flex-item :parts="smallWindow ? '12' : '4'">
        <slot name="sidebar" />
      </flex-item>
      <flex-item :parts="smallWindow ? '12' : '8'">
        <slot />
      </flex-item>
    </flex-box>
  </div>
</template>

<script lang="ts">
/**
 * Represents a grid with a sidebar that changes
 * to a stacked representation at smaller screen sizes.
 */
export default {
  name: "SidebarGrid",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { useQuasar } from "quasar";
import FlexBox from "./FlexBox.vue";
import FlexItem from "./FlexItem.vue";

const $q = useQuasar();

const smallWindow = computed(() => $q.screen.lt.lg);
</script>
