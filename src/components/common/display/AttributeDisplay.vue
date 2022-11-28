<template>
  <div>
    <typography variant="caption" :value="attribute.label" />
    <typography el="p" :value="displayValue" />
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { CustomAttributeCollection, AttributeModel } from "@/types";
import { timestampToDisplay } from "@/util";
import Typography from "./Typography.vue";

/**
 * Displays a generic attribute.
 */
export default Vue.extend({
  name: "AttributeDisplay",
  components: { Typography },
  props: {
    model: {
      type: Object as PropType<CustomAttributeCollection>,
      required: true,
    },
    attribute: {
      type: Object as PropType<AttributeModel>,
      required: true,
    },
  },
  computed: {
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
        return this.model[this.attribute.key] ? "True" : "False";
      } else {
        return value;
      }
    },
  },
});
</script>
