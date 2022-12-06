<template>
  <v-text-field
    v-if="attribute.type === 'text'"
    filled
    :label="attribute.label"
    class="mr-2"
    :rules="[lengthRules]"
    :value="model[attribute.key]"
    @input="handleInput"
  />

  <v-textarea
    v-else-if="attribute.type === 'paragraph'"
    filled
    :label="attribute.label"
    class="mr-2"
    rows="3"
    :rules="[lengthRules]"
    :value="model[attribute.key]"
    @input="handleInput"
  />

  <v-select
    v-else-if="attribute.type === 'select'"
    filled
    :label="attribute.label"
    :items="attribute.options"
    class="mr-2"
    :value="model[attribute.key]"
    @input="handleInput"
  />

  <v-autocomplete
    v-else-if="attribute.type === 'multiselect'"
    multiple
    filled
    chips
    deletable-chips
    :label="attribute.label"
    :items="attribute.options"
    class="mr-2"
    :rules="[lengthRules]"
    :value="model[attribute.key]"
    @input="handleInput"
  />

  <artifact-input
    v-else-if="attribute.type === 'relation'"
    multiple
    :label="attribute.label"
    class="mr-2 mb-2"
    :rules="[lengthRules]"
    :value="model[attribute.key]"
    @input="handleInput"
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
      :value="model[attribute.key]"
      @input="handleInput"
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
    class="mr-2"
    :rules="[intRules, numRules]"
    :value="model[attribute.key]"
    @input="handleInput"
  />

  <v-text-field
    v-else-if="attribute.type === 'float'"
    type="number"
    filled
    :label="attribute.label"
    class="mr-2"
    :rules="[numRules]"
    :value="model[attribute.key]"
    @input="handleInput"
  />

  <v-checkbox
    v-else-if="attribute.type === 'boolean'"
    :label="attribute.label"
    class="pl-4 mr-2"
    :value="model[attribute.key]"
    @change="handleInput"
  />
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import {
  AttributeCollectionSchema,
  AttributeSchema,
  AttributeDataType,
} from "@/types";
import ArtifactInput from "./ArtifactInput.vue";

/**
 * An input for a generic attribute.
 */
export default Vue.extend({
  name: "AttributeInput",
  components: { ArtifactInput },
  props: {
    model: {
      type: Object as PropType<AttributeCollectionSchema>,
      required: true,
    },
    attribute: {
      type: Object as PropType<AttributeSchema>,
      required: true,
    },
  },
  data() {
    return {
      menu: false,
    };
  },
  computed: {
    /**
     * Creates an error when an integer has a float value.
     */
    intRules(): (value: string | undefined) => string | true {
      return (value) =>
        value?.includes(".") ? "Must be a valid integer." : true;
    },
    /**
     * Creates an error when a number is not within bounds.
     */
    numRules(): (value: string | undefined) => string | true {
      return (value) => {
        const { min, max } = this.attribute;

        if (!value) {
          return true;
        } else if (max !== undefined && parseFloat(value) > max) {
          return `Value is greater than ${max}.`;
        } else if (min !== undefined && parseFloat(value) < min) {
          return `Value is less than ${min}.`;
        } else {
          return true;
        }
      };
    },
    /**
     * Creates an error when length is not within bounds.
     */
    lengthRules(): (value: string | string[] | undefined) => string | true {
      return (value) => {
        const { min, max } = this.attribute;
        const unit = Array.isArray(value) ? "items" : "characters";

        if (!value) {
          return true;
        } else if (max !== undefined && value.length > max) {
          return `Value has greater than ${max} ${unit}.`;
        } else if (min !== undefined && value.length < min) {
          return `Value has less than ${min} ${unit}.`;
        } else {
          return true;
        }
      };
    },
  },
  methods: {
    /**
     * Handles input changes to make adjustments to the stored data types.
     *
     * @param value - The updated value of this attribute.
     */
    handleInput(value: AttributeDataType): void {
      if (this.attribute.type === "int") {
        this.model[this.attribute.key] = parseInt(String(value));
      } else if (this.attribute.type === "float") {
        this.model[this.attribute.key] = parseFloat(String(value));
      } else {
        this.model[this.attribute.key] = value;
      }
    },
  },
});
</script>
