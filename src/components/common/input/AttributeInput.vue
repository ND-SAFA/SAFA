<template>
  <v-text-field
    v-if="attribute.type === 'string'"
    filled
    :label="attribute.label"
    v-model="model[attribute.key]"
    class="mr-2"
  />

  <v-select
    v-else-if="attribute.type === 'select'"
    filled
    :label="attribute.label"
    v-model="model[attribute.key]"
    :items="attribute.options"
    class="mr-2"
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
    class="mr-2"
  />

  <v-menu
    v-else-if="attribute.type === 'date'"
    ref="menu"
    v-model="menu"
    :close-on-content-click="false"
    :return-value.sync="model[attribute.key]"
    transition="scale-transition"
    offset-y
    min-width="auto"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-text-field
        filled
        v-model="model[attribute.key]"
        :label="attribute.label"
        append-icon="mdi-calendar"
        readonly
        v-bind="attrs"
        v-on="on"
        class="mr-2"
      ></v-text-field>
    </template>
    <v-date-picker
      v-model="model[attribute.key]"
      no-title
      scrollable
      color="primary"
    >
      <v-spacer></v-spacer>
      <v-btn text color="primary" @click="menu = false"> Cancel </v-btn>
      <v-btn
        text
        color="primary"
        @click="$refs.menu.save(model[attribute.key])"
      >
        OK
      </v-btn>
    </v-date-picker>
  </v-menu>

  <v-text-field
    v-else-if="attribute.type === 'int'"
    type="number"
    filled
    :label="attribute.label"
    v-model="model[attribute.key]"
    class="mr-2"
  />

  <v-text-field
    v-else-if="attribute.type === 'float'"
    type="number"
    filled
    :label="attribute.label"
    v-model="model[attribute.key]"
    class="mr-2"
  />

  <v-checkbox
    v-else-if="attribute.type === 'boolean'"
    :label="attribute.label"
    v-model="model[attribute.key]"
    class="pl-4 mr-2"
  />
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { CustomAttributeCollection, CustomAttributeModel } from "@/types";

/**
 * An input for a generic attribute.
 */
export default Vue.extend({
  name: "AttributeInput",
  props: {
    model: Object as PropType<CustomAttributeCollection>,
    attribute: Object as PropType<CustomAttributeModel>,
  },
  data() {
    return {
      menu: false,
    };
  },
});
</script>
