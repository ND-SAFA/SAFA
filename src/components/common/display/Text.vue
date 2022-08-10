<template>
  <span v-if="element === 'span'" :class="className">
    {{ value }}
  </span>
  <p v-else-if="element === 'p'" :class="className">
    {{ value }}
  </p>
  <h1 v-else-if="element === 'h1'" :class="className">
    {{ value }}
  </h1>
  <h2 v-else-if="element === 'h2'" :class="className">
    {{ value }}
  </h2>
  <h3 v-else-if="element === 'h3'" :class="className">
    {{ value }}
  </h3>
  <pre v-else-if="element === 'pre'" :class="className">
    {{ value }}
  </pre>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

type TextType = "title" | "subtitle" | "body" | "small";

type ElementType = "span" | "p" | "h1" | "h2" | "h3" | "pre";

/**
 * A generic component for displaying text.
 */
export default Vue.extend({
  name: "Text",
  props: {
    value: String,
    type: {
      type: String as PropType<TextType>,
      default: "body",
    },
    element: {
      type: String as PropType<ElementType>,
      default: "span",
    },
  },
  computed: {
    /**
     * @return The class name based on the text type.
     */
    className(): string {
      switch (this.type) {
        case "title":
          return "text-h3";
        case "subtitle":
          return "text-h4";
        case "small":
          return "text-caption";
        default:
          return "text-body-1";
      }
    },
  },
});
</script>
