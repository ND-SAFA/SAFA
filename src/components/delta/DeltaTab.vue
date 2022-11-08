<template>
  <div class="full-width mb-10">
    <delta-panel-nav />
    <artifact-deltas @open="$emit('open')" />
    <trace-deltas @open="$emit('open')" />
  </div>
</template>

<script lang="ts">
import Vue from "vue";

/**
 * Displays delta information.
 *
 * @emits `open` - On open.
 */
export default Vue.extend({
  name: "DeltaTab",
  components: {},
});
</script>
