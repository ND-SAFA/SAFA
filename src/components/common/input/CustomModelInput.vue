<template>
  <v-select
    filled
    hide-details
    label="Custom Model"
    v-model="model"
    :items="modelOptions"
    class="mr-2"
    item-value="id"
    item-text="name"
  >
    <template v-slot:item="{ item }">
      <div class="my-1">
        <typography el="div" :value="item.name" />
        <typography variant="caption" :value="item.baseModel" />
      </div>
    </template>
  </v-select>
</template>

<script lang="ts">
import Vue from "vue";
import { TrainedModel } from "@/types";
import { projectStore } from "@/hooks";
import { Typography } from "@/components/common/display";

/**
 * A selector for custom models.
 */
export default Vue.extend({
  name: "CustomModelInput",
  components: {
    Typography,
  },
  props: {
    value: String,
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
    modelOptions(): TrainedModel[] {
      return projectStore.models;
    },
  },
  watch: {
    /**
     * Updates the model if the value changes.
     */
    value(currentValue: string) {
      this.model = currentValue;
    },
    /**
     * Emits changes to the model.
     */
    model(currentValue: string) {
      this.$emit("input", currentValue);
    },
  },
});
</script>
