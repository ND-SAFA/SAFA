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
import Vue, { PropType } from "vue";
import { CustomAttributeCollection, AttributeModel } from "@/types";
import { timestampToDisplay } from "@/util";
import Typography from "./Typography.vue";
import AttributeChip from "./AttributeChip.vue";

/**
 * Displays a generic attribute.
 */
export default Vue.extend({
  name: "AttributeDisplay",
  components: { Typography, AttributeChip },
  props: {
    model: {
      type: Object as PropType<CustomAttributeCollection>,
      required: true,
    },
    attribute: {
      type: Object as PropType<AttributeModel>,
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

      return Array.isArray(value) ? value : [];
    },
    /**
     * @return The attribute's display value.
     */
    displayValue(): string {
      const value = String(this.model[this.attribute.key]);

      if (this.model[this.attribute.key] === undefined) {
        return "";
      } else if (this.attribute.type === "date") {
        return timestampToDisplay(value);
      } else if (this.attribute.type === "boolean") {
        return this.model[this.attribute.key] ? "Yes" : "No";
      } else {
        return value;
      }
    },
  },
});
</script>
