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
    <template #append>
      <icon-button
        tooltip="Read about the format of files"
        icon="info"
        @click="handleOpenWiki"
      />
      <slot name="append" />
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
import IconButton from "@/components/common/button/IconButton.vue";

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

/**
 * Opens the SAFA WIKI docs.
 */
function handleOpenWiki() {
  window.open(
    "https://www.notion.so/nd-safa/Project-Creation-5ececa9fd233437ebb37ddf893d394df#6532e1d3f983453898a8bf6ffda007f4"
  );
}
</script>
