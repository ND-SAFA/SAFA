<template>
  <attribute-grid>
    <template v-slot:item="{ attribute }">
      <attribute-display :model="model" :attribute="attribute" />
    </template>
  </attribute-grid>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { AttributeCollectionSchema } from "@/types";
import AttributeGrid from "./AttributeGrid.vue";
import AttributeDisplay from "./AttributeDisplay.vue";

/**
 * Displays a list of generic attributes.
 */
export default Vue.extend({
  name: "AttributeListDisplay",
  components: { AttributeDisplay, AttributeGrid },
  props: {
    model: Object as PropType<AttributeCollectionSchema>,
  },
});
</script>
