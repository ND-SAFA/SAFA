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
    <v-btn
      text
      small
      class="text--secondary"
      @click.stop="isExpanded = !isExpanded"
    >
      {{ isExpanded ? "See Less" : "See More" }}
    </v-btn>
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
    <v-btn
      text
      small
      class="text--secondary"
      @click.stop="isExpanded = !isExpanded"
    >
      {{ isExpanded ? "See Less" : "See More" }}
    </v-btn>
  </div>
  <!--  <pre v-else-if="variant === 'code'" :class="className">{{ value }}</pre>-->
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
import { ref, computed, withDefaults, defineProps } from "vue";
import { useTheme } from "vuetify";
import { TextAlignType, ElementType, SizeType, TextType } from "@/types";

const props = withDefaults(
  defineProps<{
    value?: string | number;
    classes?: string;
    color?: string;
    inheritColor?: boolean;
    error?: boolean;
    defaultExpanded?: boolean;
    ellipsis?: boolean;
    secondary?: boolean;
    bold?: boolean;
    wrap?: boolean;
    variant?: TextType;
    el?: ElementType;
    align?: TextAlignType;
    x?: SizeType;
    y?: SizeType;
    l?: SizeType;
    r?: SizeType;
    t?: SizeType;
    b?: SizeType;
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
  }
);

const theme = useTheme();
const isExpanded = ref(
  props.defaultExpanded && String(props.value).length < 500
);

const darkMode = computed(() => theme.global.current.value.dark);

const isExpandable = computed(() => props.variant === "expandable");

const className = computed(() => {
  let classNames = ` text-${props.align}`;

  if (props.classes) classNames += ` ${props.classes}`;
  if (props.color && !darkMode.value) classNames += ` text-${props.color}`;
  if (props.inheritColor) classNames += ` inherit-color`;
  if (props.error) classNames += ` text-error`;
  if (props.ellipsis) classNames += ` text-ellipsis`;
  if (props.secondary) classNames += ` text-secondary`;
  if (props.bold) classNames += ` font-weight-bold`;
  if (props.x) classNames += ` mx-${props.x}`;
  if (props.l) classNames += ` ml-${props.l}`;
  if (props.r) classNames += ` mr-${props.r}`;
  if (props.y) classNames += ` my-${props.y}`;
  if (props.t) classNames += ` mt-${props.t}`;
  if (props.b) classNames += ` mb-${props.b}`;
  if (props.wrap) classNames += " text-wrap";

  switch (props.variant) {
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
});
</script>
