<template>
  <span v-if="el === 'span'" :class="className">
    {{ value }}
  </span>
  <p v-else-if="el === 'p'" :class="className">
    {{ value }}
  </p>
  <h1 v-else-if="el === 'h1'" :class="className">
    {{ value }}
  </h1>
  <h2 v-else-if="el === 'h2'" :class="className">
    {{ value }}
  </h2>
  <h3 v-else-if="el === 'h3'" :class="className">
    {{ value }}
  </h3>
  <pre v-else-if="el === 'pre'" :class="className">
    {{ value }}
  </pre>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

type TextType = "large" | "title" | "subtitle" | "body" | "small";

type ElementType = "span" | "p" | "h1" | "h2" | "h3" | "pre";

type AlignType = "left" | "center" | "right";

type SizeType = "" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "10";

/**
 * A generic component for displaying text.
 */
export default Vue.extend({
  name: "Typography",
  props: {
    value: String,
    class: String,
    variant: {
      type: String as PropType<TextType>,
      default: "body",
    },
    el: {
      type: String as PropType<ElementType>,
      default: "span",
    },
    align: {
      type: String as PropType<AlignType>,
      default: "left",
    },
    x: {
      type: String as PropType<SizeType>,
      default: "",
    },
    y: {
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
  },
  computed: {
    /**
     * @return The class name based on the text type.
     */
    className(): string {
      let classNames = ` text-${this.align}`;

      if (this.class) classNames += ` ${this.class}`;
      if (this.x) classNames += ` mx-${this.x}`;
      if (this.y) classNames += ` my-${this.y}`;
      if (this.l) classNames += ` ml-${this.l}`;
      if (this.r) classNames += ` mr-${this.r}`;

      switch (this.variant) {
        case "large":
          return "text-h3" + classNames;
        case "title":
          return "text-h4" + classNames;
        case "subtitle":
          return "text-h5" + classNames;
        case "small":
          return "text-subtitle-2" + classNames;
        default:
          return "text-body-1" + classNames;
      }
    },
  },
});
</script>
