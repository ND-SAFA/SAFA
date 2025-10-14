<template>
  <div v-if="markdown" class="width-100">
    <q-markdown
      v-if="expanded"
      no-heading-anchor-links
      :src="value"
      :class="className + ' text-white-space-normal'"
    />
    <div v-else :class="className + ' text-ellipsis text-expanded'">
      {{ value }}
    </div>
    <div class="full-width flex justify-end">
      <q-btn
        v-if="props.copyable"
        flat
        dense
        round
        icon="download"
        size="sm"
        color="textCaption"
        :class="buttonClassName"
        @click.stop="handleCopy"
      />
      <q-btn
        v-if="expandable"
        flat
        dense
        size="sm"
        color="textCaption"
        :class="buttonClassName"
        @click.stop="expanded = !expanded"
      >
        {{ expandLabel }}
      </q-btn>
    </div>
  </div>
  <div v-else-if="variant === 'code'" class="width-100">
    <div class="flex nowrap overflow-auto">
      <q-btn flat dense @click.stop="expanded = !expanded">
        <q-separator vertical class="q-mx-xs" />
        <q-tooltip :delay="300"> {{ expandLabel }} </q-tooltip>
      </q-btn>
      <q-markdown v-if="expanded" no-heading-anchor-links class="full-width">
        {{ "```" + codeExt + "\n" + value + "\n```" }}
      </q-markdown>
      <div v-else :class="className + ' text-textCaption'">Code hidden</div>
    </div>
    <q-btn
      flat
      size="sm"
      dense
      color="textCaption"
      @click.stop="expanded = !expanded"
    >
      {{ expandLabel }}
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
  <a v-else-if="el === 'a'" :class="className" :href="value" target="_blank">
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
import { ref, computed, withDefaults, watch } from "vue";
import { QMarkdown } from "@quasar/quasar-ui-qmarkdown";
import { TypographyProps } from "@/types";
import { logStore, useMargins, useTheme } from "@/hooks";

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
  codeExt: "",
});

const { darkMode } = useTheme();

const buttonClassName = useMargins(props);

const className = useMargins(props, () => [
  [props.variant === "large", "text-h3"],
  [props.variant === "title", "text-h4"],
  [props.variant === "subtitle", "text-h5"],
  [props.variant === "small", "text-subtitle2"],
  [props.variant === "caption", "text-caption text-textCaption"],
  [props.variant === "code", "text-body1"],
  [
    props.variant === "body" ||
      props.variant === "expandable" ||
      props.variant === "markdown",
    "text-body1",
  ],
  [props.el === "a", "text-primary"],
  ["align", `text-${props.align}`],
  [!!props.color && !darkMode.value, `text-${props.color}`],
  ["inheritColor", "inherit-color"],
  ["error", "text-negative"],
  ["ellipsis", "text-ellipsis"],
  ["secondary", "text-textCaption"],
  ["bold", "text-bold"],
  ["small", "text-sm"],
  ["large", "text-lg"],
  ["wrap", "text-white-space-normal"],
  ["class", props.class],
]);

const baseExpanded = computed(
  () =>
    props.variant === "markdown" ||
    (props.defaultExpanded &&
      props.variant !== "code" &&
      (props.collapseLength === 0 ||
        String(props.value).length < props.collapseLength))
);

const expanded = ref(baseExpanded.value);

const markdown = computed(
  () => props.variant === "expandable" || props.variant === "markdown"
);

const expandable = computed(() => props.variant === "expandable");

const expandLabel = computed(() => (expanded.value ? "See Less" : "See More"));

const codeExt = computed(() => {
  if (!props.codeExt) {
    return "";
  } else {
    return (
      {
        cpp: "clike",
        cc: "clike",
        c: "clike",
        h: "clike",
        js: "js",
        ts: "js",
        vue: "vue",
        java: "clike",
        py: "python",
      }[props.codeExt] || ""
    );
  }
});

/**
 * Copy the text to the clipboard.
 */
function handleCopy() {
  navigator.clipboard.writeText(String(props.value));
  logStore.onInfo("Copied to clipboard");
}

/**
 * When the variant or value changes, reset the expanded state.
 */
watch(
  () => [props.value, props.variant],
  () => (expanded.value = baseExpanded.value)
);
</script>
