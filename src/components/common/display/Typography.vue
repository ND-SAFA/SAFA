<template>
  <div v-if="isExpandable" style="width: 100%">
    <div v-if="isExpanded" :class="className" style="white-space: normal">
      {{ value }}
    </div>
    <div
      v-else
      :class="className + ' text-ellipsis'"
      style="white-space: nowrap; width: inherit"
    >
      {{ value }}
    </div>
    <v-btn
      text
      small
      @click.stop="isExpanded = !isExpanded"
      class="text--secondary"
    >
      {{ isExpanded ? "See Less" : "See More" }}
    </v-btn>
  </div>
  <pre v-else-if="variant === 'code'" :class="className">
     {{ value }}
  </pre>
  <span v-else-if="el === 'span'" :class="className">
    {{ value }}
  </span>
  <p v-else-if="el === 'p'" :class="className">
    {{ value }}
  </p>
  <div v-else-if="el === 'div'" :class="className">
    {{ value }}
  </div>
  <h1 v-else-if="el === 'h1'" :class="className">
    {{ value }}
  </h1>
  <h2 v-else-if="el === 'h2'" :class="className">
    {{ value }}
  </h2>
  <h3 v-else-if="el === 'h3'" :class="className">
    {{ value }}
  </h3>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { AlignType, ElementType, SizeType, TextType } from "@/types";

/**
 * A generic component for displaying text.
 */
export default Vue.extend({
  name: "Typography",
  props: {
    value: String,
    classes: String,
    color: String,
    error: Boolean,
    defaultExpanded: Boolean,
    ellipsis: Boolean,
    secondary: Boolean,
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
  data() {
    return {
      isExpanded: this.defaultExpanded && this.value.length < 500,
    };
  },
  computed: {
    /**
     * @return Whether this text is expandable.
     */
    isExpandable(): boolean {
      return this.variant === "expandable";
    },
    /**
     * @return The class name.
     */
    className(): string {
      let classNames = ` text-${this.align}`;

      if (this.classes) classNames += ` ${this.classes}`;
      if (this.color) classNames += ` ${this.color}--text`;
      if (this.error) classNames += ` error--text`;
      if (this.ellipsis) classNames += ` text-ellipsis`;
      if (this.secondary) classNames += ` text--secondary`;
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
        case "caption":
          return "text-caption text--secondary" + classNames;
        case "code":
          return "text-body-1 overflow-y-auto" + classNames;
        default:
          return "text-body-1" + classNames;
      }
    },
  },
});
</script>
