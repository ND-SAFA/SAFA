<template>
  <v-combobox
    filled
    ref="artifactTypeInput"
    :label="label"
    :multiple="multiple"
    v-model="model"
    :items="types"
    :hint="hint"
    :hide-details="hideDetails"
    :persistent-hint="persistentHint"
    :error-messages="errorMessages"
    item-text="label"
    item-value="type"
    @blur="$emit('blur')"
    @submit="$emit('blur')"
  >
    <template v-slot:append>
      <icon-button
        small
        icon-id="mdi-content-save-outline"
        tooltip="Save Types"
        data-cy="button-save-types"
        @click="handleClose"
      />
    </template>
    <template v-slot:selection="{ item }">
      <attribute-chip artifact-type :value="item" />
    </template>
  </v-combobox>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { typeOptionsStore } from "@/hooks";
import { IconButton } from "@/components/common/button";
import { AttributeChip } from "@/components/common/display";

/**
 * An input for selecting artifact types.
 *
 * @emits-1 `blur` - On input blur.
 * @emits-2 `input` (string[] | string | undefined) - On input change.
 */
export default Vue.extend({
  name: "ArtifactTypeInput",
  components: { AttributeChip, IconButton },
  props: {
    value: {
      type: [Array, String] as PropType<string[] | string | null>,
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
    hideDetails: Boolean,
    errorMessages: Array,
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
    types(): string[] {
      return typeOptionsStore.artifactTypes;
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
    value(currentValue: string[] | string | null) {
      this.model = currentValue;
    },
    /**
     * Emits changes to the model.
     */
    model(currentValue: string[] | string | null) {
      this.$emit("input", currentValue);
    },
  },
});
</script>

<style scoped></style>
