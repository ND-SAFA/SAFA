<template>
  <attribute-grid>
    <template v-slot:item="{ attribute }">
      <attribute-input :model="model" :attribute="attribute" />
    </template>
  </attribute-grid>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { AttributeCollectionSchema } from "@/types";
import { AttributeGrid } from "@/components/common/display";
import AttributeInput from "./AttributeInput.vue";

/**
 * A list of inputs for a list of generic attributes.
 */
export default Vue.extend({
  name: "AttributeListInput",
  components: { AttributeGrid, AttributeInput },
  props: {
    model: Object as PropType<AttributeCollectionSchema>,
  },
});
</script>
