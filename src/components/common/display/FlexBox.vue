<template>
  <div :class="className" :style="style">
    <slot />
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { AlignType, JustifyType } from "@/types";

/**
 * A generic component for displaying flex content.
 */
export default Vue.extend({
  name: "FlexBox",
  props: {
    align: {
      type: String as PropType<AlignType>,
      default: "left",
    },
    justify: {
      type: String as PropType<JustifyType>,
      default: "start",
    },
    maxWidth: Number,
  },
  computed: {
    /**
     * @return The class name.
     */
    style(): string {
      if (this.maxWidth) {
        return `max-width: ${this.maxWidth}px`;
      } else {
        return "";
      }
    },
    /**
     * @return The class name.
     */
    className(): string {
      let classNames = `d-flex `;

      if (this.align) classNames += ` align-${this.align}`;
      if (this.justify) classNames += ` justify-${this.justify}`;

      return classNames;
    },
  },
});
</script>

<style scoped></style>
