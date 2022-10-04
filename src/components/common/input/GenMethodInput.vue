<template>
  <v-select
    filled
    hide-details
    label="Model"
    v-model="model"
    :items="modelOptions"
    class="mr-2"
    item-value="id"
    item-text="id"
  >
    <template v-slot:item="{ item }">
      <div class="my-1">
        <typography el="div" :value="item.id" />
        <typography variant="caption" :value="item.name" />
      </div>
    </template>
  </v-select>
</template>

<script lang="ts">
import Vue from "vue";
import { ModelType, SelectOption } from "@/types";
import { traceModelOptions } from "@/util";
import { Typography } from "@/components/common/display";

/**
 * A selector for trace generation methods.
 */
export default Vue.extend({
  name: "GenMethodInput",
  components: {
    Typography,
  },
  props: {
    value: String,
    onlyTrainable: Boolean,
  },
  data() {
    return {
      model: this.value,
    };
  },
  computed: {
    /**
     * @return The trace generation model types.
     */
    modelOptions(): SelectOption[] {
      return this.onlyTrainable
        ? traceModelOptions().slice(0, 3)
        : traceModelOptions();
    },
  },
  watch: {
    /**
     * Updates the model if the value changes.
     */
    value(currentValue: ModelType) {
      this.model = currentValue;
    },
    /**
     * Emits changes to the model.
     */
    model(currentValue: ModelType) {
      this.$emit("input", currentValue);
    },
  },
});
</script>
