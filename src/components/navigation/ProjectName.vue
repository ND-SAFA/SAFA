<template>
  <h1 :style="`font-size: 16pt; color: ${color}`">SAFA</h1>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  props: {
    color: String,
  },
});
</script>
