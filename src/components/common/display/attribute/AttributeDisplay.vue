<template>
  <div>
    <typography
      v-if="props.showName"
      variant="caption"
      :value="attribute.label"
    />
    <div v-if="arrayValue.length > 0">
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
import { AttributeCollectionSchema, AttributeSchema } from "@/types";
import { timestampToDisplay } from "@/util";
import { artifactStore } from "@/hooks";
import { Typography } from "../content";
import { AttributeChip } from "../chip";

const props = defineProps<{
  /**
   * The collection of attribute values to display from.
   */
  values: AttributeCollectionSchema;
  /**
   * The attribute from the collection to display.
   */
  attribute: AttributeSchema;
  /**
   * If true, the attribute name will be displayed above the value.
   */
  showName?: boolean;
}>();

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
