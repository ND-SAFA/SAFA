<template>
  <div v-if="isExpandable" class="width-100">
    <div v-if="isExpanded" :class="className + ' text-white-space-normal'">
      {{ value }}
    </div>
    <div v-else :class="className + ' text-ellipsis text-expanded'">
      {{ value }}
    </div>
    <q-btn flat size="sm" color="grey-8" @click.stop="isExpanded = !isExpanded">
      {{ isExpanded ? "See Less" : "See More" }}
    </q-btn>
  </div>
  <div v-else-if="variant === 'code'" class="width-100">
    <pre v-if="isExpanded" v-highlightjs :class="className">
      <code>{{value}}</code>
    </pre>
    <div v-else :class="className + ' text-grey-8'">
      Code is hidden to save space.
    </div>
    <q-btn flat size="sm" color="grey-8" @click.stop="isExpanded = !isExpanded">
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
  <a v-else-if="el === 'a'" :class="className" :href="value">
    {{ value }}
  </a>
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
import { TypographyProps } from "@/types";
import { useMargins, useTheme } from "@/hooks";

const props = withDefaults(defineProps<TypographyProps>(), {
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
  collapseLength: 500,
});

const { darkMode } = useTheme();

const className = useMargins(props, () => [
  [props.variant === "large", "text-h3"],
  [props.variant === "title", "text-h4"],
  [props.variant === "subtitle", "text-h5"],
  [props.variant === "small", "text-subtitle2"],
  [props.variant === "caption", "text-caption text-grey-8"],
  [props.variant === "code", "text-body1"],
  [props.variant === "body" || props.variant === "expandable", "text-body1"],
  ["align", `text-${props.align}`],
  [!!props.color && !darkMode.value, `text-${props.color}`],
  ["inheritColor", "inherit-color"],
  ["error", "text-negative"],
  ["ellipsis", "text-ellipsis"],
  ["secondary", "text-grey-8"],
  ["bold", "text-bold"],
  ["small", "text-sm"],
  ["large", "text-lg"],
  ["wrap", "text-wrap"],
  ["class", props.class],
]);

const isExpanded = ref(
  props.defaultExpanded &&
    (props.collapseLength === 0 ||
      String(props.value).length < props.collapseLength)
);

const isExpandable = computed(() => props.variant === "expandable");
</script>
