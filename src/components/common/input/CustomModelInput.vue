<template>
  <v-select
    filled
    hide-details
    label="Custom Model"
    v-model="model"
    :items="modelOptions"
    class="mr-2"
    item-text="name"
    item-value="id"
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
import Vue, { PropType } from "vue";
import { GenerationModel } from "@/types";
import { projectStore } from "@/hooks";
import { Typography } from "@/components/common/display";

/**
 * A selector for custom models.
 *
 * @emits-1 `input` (TrainedModel | undefined) - On value change.
 */
export default Vue.extend({
  name: "CustomModelInput",
  components: {
    Typography,
  },
  props: {
    value: Object as PropType<GenerationModel | undefined>,
  },
  data() {
    return {
      model: this.value?.id,
    };
  },
  computed: {
    /**
     * @return The trace generation model types.
     */
    modelOptions(): GenerationModel[] {
      return projectStore.models;
    },
  },
  watch: {
    /**
     * Updates the model if the value changes.
     */
    value(currentValue: GenerationModel) {
      this.model = currentValue?.id;
    },
    /**
     * Emits changes to the model.
     */
    model(currentId: string) {
      this.$emit(
        "input",
        projectStore.models.find(({ id }) => id === currentId)
      );
    },
  },
});
</script>
