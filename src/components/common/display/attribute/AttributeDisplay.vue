<template>
  <div>
    <typography v-if="!hideTitle" variant="caption" :value="attribute.label" />
    <div v-if="arrayValue.length > 0">
      <attribute-chip v-for="value in arrayValue" :key="value" :value="value" />
    </div>
    <typography v-else el="p" :value="displayValue" />
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { AttributeCollectionSchema, AttributeSchema } from "@/types";
import { timestampToDisplay } from "@/util";
import { artifactStore } from "@/hooks";
import Typography from "../Typography.vue";
import AttributeChip from "./AttributeChip.vue";

/**
 * Displays a generic attribute.
 */
export default defineComponent({
  name: "AttributeDisplay",
  components: { Typography, AttributeChip },
  props: {
    model: {
      type: Object as PropType<AttributeCollectionSchema>,
      required: true,
    },
    attribute: {
      type: Object as PropType<AttributeSchema>,
      required: true,
    },
    hideTitle: Boolean,
  },
  computed: {
    /**
     * @return The attribute's array value, if it is an array.
     */
    arrayValue(): string[] {
      const value = this.model[this.attribute.key];
      const array = Array.isArray(value) ? value : [];

      return this.attribute.type === "relation"
        ? array.map((id) => artifactStore.getArtifactById(id)?.name || id)
        : array;
    },
    /**
     * @return The attribute's display value.
     */
    displayValue(): string {
      const value = String(this.model[this.attribute.key]);

      if (this.model[this.attribute.key] === undefined) {
        return "";
      } else if (this.attribute.type === "date") {
        return timestampToDisplay(value).split(" at ")[0];
      } else if (this.attribute.type === "boolean") {
        return this.model[this.attribute.key] ? "Yes" : "No";
      } else {
        return value;
      }
    },
  },
});
</script>
