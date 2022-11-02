<template>
  <v-text-field
    v-if="attribute.type === 'string'"
    filled
    :label="attribute.label"
    v-model="model[attribute.key]"
  />
  <v-text-field
    v-else-if="attribute.type === 'number'"
    type="number"
    filled
    :label="attribute.label"
    v-model="model[attribute.key]"
  />
  <v-select
    v-else-if="attribute.type === 'select'"
    filled
    :label="attribute.label"
    v-model="model[attribute.key]"
    :items="attribute.options"
  />
  <v-autocomplete
    v-else-if="attribute.type === 'multiselect'"
    multiple
    filled
    chips
    deletable-chips
    :label="attribute.label"
    v-model="model[attribute.key]"
    :items="attribute.options"
  />
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { CustomAttributeModel } from "@/types";

/**
 * An input for a generic attribute.
 */
export default Vue.extend({
  name: "AttributeInput",
  props: {
    model: Object,
    attribute: Object as PropType<CustomAttributeModel>,
  },
});
</script>
