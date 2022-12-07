<template>
  <v-file-input
    clearable
    filled
    small-chips
    label="Upload Files"
    :multiple="multiple"
    truncate-length="30"
    class="mt-4"
    v-model="model"
    :data-cy="dataCy"
    :error-messages="errors"
    @click:clear="$emit('clear')"
  />
</template>

<script lang="ts">
import Vue, { PropType } from "vue";

/**
 * Displays a generic file selector.
 *
 * @emits-1 `clear` - On clear.
 * @emits-2 `input` (File[] | File | null) - On file change.
 */
export default Vue.extend({
  name: "FileInput",
  props: {
    value: Array as PropType<File[] | File | null>,
    multiple: {
      type: Boolean,
      required: false,
      default: true,
    },
    dataCy: {
      type: String,
      default: "input-files",
    },
    errors: {
      type: Array as PropType<string[]>,
      default: () => [],
    },
  },
  data() {
    return {
      model: this.value,
    };
  },
  watch: {
    /**
     * Updates the model if the value changes.
     */
    value(currentValue: File[] | File | null) {
      this.model = currentValue;
    },
    /**
     * Emits changes to the model.
     */
    model(currentValue: File[] | File | null) {
      this.$emit("input", currentValue);
    },
  },
});
</script>
