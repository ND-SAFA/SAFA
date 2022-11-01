<template>
  <flex-box column>
    <attribute-input
      v-for="attribute of attributes"
      :key="attribute.key"
      :model="model"
      :attribute="attribute"
    />
  </flex-box>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { AttributeModel } from "@/types";
import { FlexBox } from "@/components/common/display";
import AttributeInput from "./AttributeInput.vue";

/**
 * A list of inputs for a list of generic attributes.
 */
export default Vue.extend({
  name: "AttributeListInput",
  components: { FlexBox, AttributeInput },
  props: {
    model: Object,
    attributes: Array as PropType<AttributeModel[]>,
  },
});
</script>
