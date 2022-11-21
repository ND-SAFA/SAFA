<template>
  <v-alert border="left" color="warning" class="mt-2">
    <typography
      color="white"
      value="This content is still under construction. Check back soon!"
    />
  </v-alert>
</template>

<script lang="ts">
import Vue from "vue";
import Typography from "./Typography.vue";

/**
 * An alert for components that are still under construction.
 */
export default Vue.extend({
  name: "UnderConstructionAlert",
  components: { Typography },
});
</script>
