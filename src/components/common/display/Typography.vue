<template>
  <div v-if="isExpandable" style="width: 100%">
    <div v-if="isExpanded" :class="className" style="white-space: normal">
      {{ value }}
    </div>
    <div
      v-else
      :class="className + ' text-ellipsis'"
      style="white-space: nowrap; width: inherit; max-width: 60vw"
    >
      {{ value }}
    </div>
    <q-btn flat size="sm" @click.stop="isExpanded = !isExpanded">
      {{ isExpanded ? "See Less" : "See More" }}
    </q-btn>
  </div>
  <div v-else-if="variant === 'code'" style="width: 100%">
    <pre v-if="isExpanded" :class="className">{{ value }}</pre>
    <div
      v-else
      :class="className + ' text-ellipsis'"
      style="white-space: nowrap; width: inherit; max-width: 60vw"
    >
      {{ value }}
    </div>
    <q-btn flat size="sm" @click.stop="isExpanded = !isExpanded">
      {{ isExpanded ? "See Less" : "See More" }}
    </q-btn>
  </div>
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
/**
 * A generic component for displaying text.
 */
export default {
  name: "Typography",
};
</script>

<script setup lang="ts">
import { ref, computed, withDefaults } from "vue";
import {
  ElementType,
  SizeType,
  TextAlignType,
  TextType,
  ThemeColor,
} from "@/types";
import { useMargins, useTheme } from "@/hooks";

const props = withDefaults(
  defineProps<{
    /**
     * The text value to display.
     */
    value?: string | number;
    /**
     * Whether to truncate text with an ellipsis.
     */
    ellipsis?: boolean;

    /**
     * Whether to inherit color from the parent element.
     */
    inheritColor?: boolean;
    /**
     * Whether to color this text as an error.
     */
    error?: boolean;
    /**
     * Renders the text with a faded color.
     */
    secondary?: boolean;
    /**
     * The color to render the component with.
     */
    color?: ThemeColor;

    /**
     * Bolds the text.
     */
    bold?: boolean;
    /**
     * Sets the text to wrap.
     */
    wrap?: boolean;

    /**
     * The variant of text to render.
     * @default `body`
     */
    variant?: TextType;
    /**
     * The element to render the text on.
     * @default `span`
     */
    el?: ElementType;
    /**
     * How to align the text.
     * @default `left`
     */
    align?: TextAlignType;

    /**
     * For expandable variants, whether the content defaults to expanded.
     */
    defaultExpanded?: boolean;

    /**
     * Renders a smaller component.
     */
    small?: boolean;
    /**
     * Renders a larger component.
     */
    large?: boolean;

    /**
     * The x margin.
     */
    x?: SizeType;
    /**
     * The y margin.
     */
    y?: SizeType;
    /**
     * The left margin.
     */
    l?: SizeType;
    /**
     * The right margin.
     */
    r?: SizeType;
    /**
     * The top margin.
     */
    t?: SizeType;
    /**
     * The bottom margin.
     */
    b?: SizeType;

    /**
     * The classnames to include on this component.
     */
    class?: string;
  }>(),
  {
    value: "",
    classes: undefined,
    color: undefined,
    variant: "body",
    el: "span",
    align: "left",
    x: "",
    y: "",
    l: "",
    r: "",
    t: "",
    b: "",
    class: "",
  }
);

const { darkMode } = useTheme();

const className = useMargins(props, () => [
  [props.variant === "large", "text-h3"],
  [props.variant === "title", "text-h4"],
  [props.variant === "subtitle", "text-h5"],
  [props.variant === "small", "text-subtitle2"],
  [props.variant === "caption", "text-caption"],
  [props.variant === "code", "text-body1 overflow-y-auto"],
  [props.variant === "body" || props.variant === "expandable", "text-body1"],
  ["align", `text-${props.align}`],
  [!!props.color && !darkMode.value, `text-${props.color}`],
  ["inheritColor", "inherit-color"],
  ["error", "text-negative"],
  ["ellipsis", "text-ellipsis"],
  ["secondary", "text-grey"],
  ["bold", "font-weight-bold"],
  ["small", "text-sm"],
  ["large", "text-lg"],
  ["wrap", "text-wrap"],
  ["class", props.class],
]);

const isExpanded = ref(
  props.defaultExpanded && String(props.value).length < 500
);

const isExpandable = computed(() => props.variant === "expandable");
</script>
