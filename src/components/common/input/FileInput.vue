<template>
  <q-file
    v-model="model"
    clearable
    filled
    use-chips
    :label="label"
    :multiple="props.multiple"
    :error-message="props.errorMessage || ''"
    :error="showError"
    :data-cy="props.dataCy"
    hint="File Types: .csv, .json"
    @clear="$emit('clear')"
  >
    <template #prepend>
      <icon variant="file" />
    </template>
  </q-file>
</template>

<script lang="ts">
/**
 * Displays a generic file selector.
 */
export default {
  name: "FileInput",
};
</script>

<script setup lang="ts">
import { computed, withDefaults } from "vue";
import { FileInputProps } from "@/types";
import { useVModel } from "@/hooks";
import { Icon } from "@/components/common/display";

const props = withDefaults(defineProps<FileInputProps>(), {
  dataCy: "input-files",
  errorMessage: undefined,
  modelValue: undefined,
});

defineEmits<{
  (e: "clear"): void;
  (e: "update:modelValue", files: File | File[] | null | undefined): void;
}>();

const model = useVModel(props, "modelValue");

const showError = computed(
  () => !!props.errorMessage && props.errorMessage.length > 0
);
const label = computed(() => (props.multiple ? "Upload Files" : "Upload File"));
</script>
