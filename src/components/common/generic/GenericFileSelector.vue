<template>
  <v-file-input
    small-chips
    :multiple="multiple"
    truncate-length="30"
    clearable
    outlined
    class="mt-3"
    @change="onChangeFiles"
    @click:clear="$emit('onClear')"
  />
</template>

<script lang="ts">
import Vue from "vue";
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
    onChangeFiles(files: File[]) {
      this.$emit("onChangeFiles", files);
    },
  },
});
</script>
