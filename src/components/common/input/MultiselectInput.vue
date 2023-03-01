<template>
  <q-select
    v-model="model"
    multiple
    filled
    use-chips
    use-input
    :label="props.label"
    :options="props.options"
    :option-label="props.optionsLabel"
    :data-cy="props.dataCy"
    :error-message="props.errorMessage || ''"
    :error="showError"
    :class="className"
    :hint="props.hint"
    :new-value-mode="props.addValues ? 'add-unique' : ''"
  />
</template>

<script lang="ts">
/**
 * A generic multiselect input.
 */
export default {
  name: "MultiselectInput",
};
</script>

<script setup lang="ts">
import { withDefaults, computed } from "vue";
import { SizeType } from "@/types";
import { useMargins, useVModel } from "@/hooks";

const props = withDefaults(
  defineProps<{
    /**
     * The model value.
     */
    modelValue: unknown[];
    /**
     * The options to select from.
     */
    options: unknown[];
    /**
     * Returns the display name of an option.
     */
    optionsLabel?: (option: unknown) => string;
    /**
     * An error message to display, if one exists.
     */
    errorMessage?: string | false;
    /**
     * The classnames to include on this component.
     */
    class?: string;
    /**
     * The label to display.
     */
    label?: string;
    /**
     * The bottom margin.
     */
    b?: SizeType;
    /**
     * A hint to display below the input.
     */
    hint?: string;
    /**
     * A testing selector.
     */
    dataCy?: string;
    /**
     * If true, new options can be created by pressing enter.
     */
    addValues?: boolean;
  }>(),
  {
    b: "1",
    label: "",
    errorMessage: "",
    class: "",
    hint: undefined,
    dataCy: undefined,
    optionsLabel: undefined,
  }
);

defineEmits<{
  /**
   * Called when the model is updated.
   */
  (e: "update:modelValue"): void;
}>();

const model = useVModel(props, "modelValue");

const className = useMargins(props, () => [[!!props.class, props.class]]);

const showError = computed(
  () => !!props.errorMessage && props.errorMessage.length > 0
);
</script>
