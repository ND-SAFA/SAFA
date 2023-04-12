<template>
  <div>
    <slot name="header" />
    <flex-box :column="smallWindow">
      <flex-item
        :parts="smallWindow ? '12' : '4'"
        :full-width="smallWindow"
        :class="smallWindow ? '' : 'q-pr-md'"
      >
        <slot name="sidebar" />
      </flex-item>
      <flex-item :parts="smallWindow ? '12' : '8'" :full-width="smallWindow">
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
import { useScreen } from "@/hooks";
import { FlexBox, FlexItem } from "@/components/common/display";

const { smallWindow } = useScreen();
</script>
