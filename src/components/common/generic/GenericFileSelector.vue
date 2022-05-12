<template>
  <v-file-input
    clearable
    outlined
    small-chips
    label="Upload Files"
    :multiple="multiple"
    truncate-length="30"
    class="mt-3"
    @change="handleChangeFiles"
    @click:clear="$emit('clear')"
  />
</template>

<script lang="ts">
import Vue from "vue";

/**
 * Displays a generic file selector.
 *
 * @emits-1 `clear` - On clear.
 * @emits-2 `change:files` - On file change.
 */
export default Vue.extend({
  name: "GenericFileSelector",
  props: {
    multiple: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  methods: {
    /**
     * Emits files when the change.
     * @param files - The updated files.
     */
    handleChangeFiles(files: File[]) {
      this.$emit("change:files", files);
    },
  },
});
</script>
