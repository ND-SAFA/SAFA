<template>
  <v-autocomplete
    filled
    :label="label"
    :multiple="multiple"
    v-model="model"
    :items="typeDirections"
    :hint="hint"
    :persistent-hint="persistentHint"
    item-text="label"
    item-value="type"
    @blur="$emit('blur')"
  >
    <template v-slot:selection="{ item }">
      <attribute-chip artifact-type :value="item.type" />
    </template>
  </v-autocomplete>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { typeOptionsStore } from "@/hooks";
import { LabelledTraceDirectionModel } from "@/types";
import AttributeChip from "@/components/common/display/AttributeChip.vue";

/**
 * An input for selecting artifact types.
 *
 * @emits-1 `blur` - On input blur.
 */
export default Vue.extend({
  name: "ArtifactTypeInput",
  components: { AttributeChip },
  props: {
    value: {
      type: [Array, String] as PropType<string[] | string | undefined>,
      required: false,
    },
    multiple: {
      type: Boolean,
      default: false,
    },
    label: {
      type: String,
      default: "Artifact Types",
    },
    hint: String,
    persistentHint: Boolean,
  },
  data() {
    return {
      model: this.value,
    };
  },
  computed: {
    /**
     * @return The current project's artifact types.
     */
    typeDirections(): LabelledTraceDirectionModel[] {
      return typeOptionsStore.typeDirections();
    },
  },
  watch: {
    /**
     * Updates the model if the value changes.
     */
    value(currentValue: string[] | string | undefined) {
      this.model = currentValue;
    },
    /**
     * Emits changes to the model.
     */
    model(currentValue: string[] | string | undefined) {
      this.$emit("input", currentValue);
    },
  },
});
</script>

<style scoped></style>
