<template>
  <v-autocomplete
    filled
    ref="artifactTypeInput"
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
    <template v-slot:append>
      <generic-icon-button
        small
        icon-id="mdi-content-save-outline"
        tooltip="Save Types"
        @click="handleClose"
      />
    </template>
    <template v-slot:selection="{ item }">
      <attribute-chip artifact-type :value="item.type" />
    </template>
  </v-autocomplete>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { LabelledTraceDirectionModel } from "@/types";
import { typeOptionsStore } from "@/hooks";
import { GenericIconButton } from "@/components/common/generic";
import AttributeChip from "@/components/common/display/AttributeChip.vue";

/**
 * An input for selecting artifact types.
 *
 * @emits-1 `blur` - On input blur.
 */
export default Vue.extend({
  name: "ArtifactTypeInput",
  components: { AttributeChip, GenericIconButton },
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
  methods: {
    /**
     * Closes the selection window.
     */
    handleClose(): void {
      (this.$refs.artifactTypeInput as HTMLElement).blur();
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
