<template>
  <q-select
    v-model="model"
    multiple
    :filled="!props.outlined"
    :outlined="props.outlined"
    use-chips
    use-input
    :label="props.label"
    :options="options"
    :option-value="props.optionValue"
    :option-label="props.optionLabel"
    :map-options="props.optionToValue"
    :emit-value="props.optionToValue"
    :data-cy="props.dataCy"
    :error-message="props.errorMessage || undefined"
    :error="showError"
    :class="className"
    :hint="props.hint"
    :new-value-mode="props.addValues ? 'add-unique' : undefined"
    input-debounce="0"
    :clearable="props.clearable"
    @filter="filter"
  >
    <template #prepend>
      <slot name="prepend" />
    </template>
  </q-select>
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
import { withDefaults, computed, ref, watch } from "vue";
import { SelectOption, SizeType } from "@/types";
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
    options: string[] | SelectOption[] | unknown[];
    /**
     * The key of an option's id.
     */
    optionValue?: string | ((opt: unknown) => string);
    /**
     * The key of an option's display label.
     */
    optionLabel?: string | ((opt: unknown) => string);
    /**
     * Only saves the option's value, not the entire object.
     */
    optionToValue?: boolean;
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
    /**
     * Whether to display as outlined, instead of the default filled.
     */
    outlined?: boolean;
    /**
     * Whether to display a button to clear the input.
     */
    clearable?: boolean;
  }>(),
  {
    b: "1",
    label: "",
    errorMessage: "",
    class: "",
    hint: undefined,
    dataCy: undefined,
    optionLabel: undefined,
    optionValue: undefined,
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
  () => (!!props.errorMessage && props.errorMessage.length > 0) || undefined
);

const options = ref(props.options);

/**
 * Filters the artifact type options.
 * @param searchText - The search text to filter with.
 * @param update - A function call to update the options.
 */
function filter(
  searchText: string | null,
  update: (fn: () => void) => void
): void {
  update(() => {
    if (!searchText) {
      options.value = props.options;
    } else {
      const lowercaseSearchText = searchText.toLowerCase();

      options.value = props.options.filter(
        (option: string | SelectOption | unknown) => {
          const value =
            !!option && typeof option === "object" && "name" in option
              ? String(option.name)
              : String(option);

          return value.toLowerCase().includes(lowercaseSearchText);
        }
      );
    }
  });
}

watch(
  () => props.options,
  (newOptions) => (options.value = newOptions)
);
</script>
