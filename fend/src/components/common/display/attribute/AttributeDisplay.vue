<template>
  <div :data-cy="dataCy">
    <typography
      v-if="props.showName"
      variant="caption"
      :value="attribute.label"
    />
    <p v-if="isLink">
      <typography el="a" :value="displayValue" />
    </p>
    <div v-else-if="arrayValue.length > 0">
      <attribute-chip v-for="value in arrayValue" :key="value" :value="value" />
    </div>
    <typography v-else el="p" :value="displayValue" />
  </div>
</template>

<script lang="ts">
/**
 * Displays a generic attribute.
 */
export default {
  name: "AttributeDisplay",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { AttributeDisplayProps } from "@/types";
import { timestampToDisplay } from "@/util";
import { artifactStore } from "@/hooks";
import { Typography } from "../content";
import { AttributeChip } from "../chip";

const props = defineProps<AttributeDisplayProps>();

const dataCy = computed(() => `text-attribute-${props.attribute.key}`);
const isLink = computed(() =>
  String(props.values[props.attribute.key]).includes("://")
);

/**
 * The display values for an array attribute.
 */
const arrayValue = computed(() => {
  const value = props.values[props.attribute.key];
  const array = Array.isArray(value) ? value : [];

  return props.attribute.type === "relation"
    ? array.map((id) => artifactStore.getArtifactById(id)?.name || id)
    : array;
});

/**
 * The display values for all non-array attributes.
 */
const displayValue = computed(() => {
  const stringValue = String(props.values[props.attribute.key]);

  if (props.values[props.attribute.key] === undefined) {
    return "";
  } else if (props.attribute.type === "date") {
    return timestampToDisplay(stringValue).split(" at ")[0];
  } else if (props.attribute.type === "boolean") {
    return props.values[props.attribute.key] ? "Yes" : "No";
  } else {
    return stringValue;
  }
});
</script>
