<template>
  <div :class="className" :style="style">
    <slot />
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { JustifyType, SizeType, AlignType } from "@/types";

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
    x: {
      type: String as PropType<SizeType>,
      default: "",
    },
    l: {
      type: String as PropType<SizeType>,
      default: "",
    },
    r: {
      type: String as PropType<SizeType>,
      default: "",
    },
    y: {
      type: String as PropType<SizeType>,
      default: "",
    },
    t: {
      type: String as PropType<SizeType>,
      default: "",
    },
    b: {
      type: String as PropType<SizeType>,
      default: "",
    },
    maxWidth: Number,
    fullWidth: Boolean,
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
      if (this.fullWidth) classNames += ` full-width`;
      if (this.x) classNames += ` mx-${this.x}`;
      if (this.l) classNames += ` ml-${this.l}`;
      if (this.r) classNames += ` mr-${this.r}`;
      if (this.y) classNames += ` my-${this.y}`;
      if (this.t) classNames += ` mt-${this.t}`;
      if (this.b) classNames += ` mb-${this.b}`;

      return classNames;
    },
  },
});
</script>

<style scoped></style>
