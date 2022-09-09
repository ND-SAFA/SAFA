<template>
  <v-select
    filled
    hide-details
    label="Model"
    v-model="model"
    :items="modelOptions"
    class="mr-2"
    item-value="id"
    item-text="name"
  >
    <template v-slot:item="{ item }">
      <div class="my-1">
        <typography el="div" :value="item.name" />
        <typography variant="caption" :value="getModelDetails(item.id)" />
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
  },
  computed: {
    /**
     * @return The trace generation model types.
     */
    modelOptions(): SelectOption[] {
      return traceModelOptions();
    },
    model: {
      get(): string {
        return this.value;
      },
      set(newValue: string): void {
        this.$emit("update:value", newValue);
      },
    },
  },
  methods: {
    /**
     * @return The detail method for a model.
     */
    getModelDetails(method: ModelType | ""): string {
      if (method === ModelType.VSM) {
        return (
          "Faster, lower quality links. The vector-space model computes the similarity of two documents " +
          "using their word counts with common words account for."
        );
      } else if (method === ModelType.TBERT) {
        return (
          "Slower, higher quality links. A deep-learning algorithm leveraging a RoBERTa model trained " +
          "on open source projects for trace link prediction."
        );
      } else {
        return "";
      }
    },
  },
});
</script>
