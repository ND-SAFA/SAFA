<template>
  <v-file-input
    chips
    multiple
    truncate-length="30"
    clearable
    outlined
    class="mt-3"
    @change="onChangeFiles"
  ></v-file-input>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  methods: {
    onChangeFiles(files: File[]) {
      this.$emit("onChangeFiles", files);
    },
  },
});
</script>
