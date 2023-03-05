<template>
  <alert
    type="warning"
    message="This content is still under construction. Check back soon!"
    class="q-my-md"
  />
</template>

<script lang="ts">
/**
 * An alert for components that are still under construction.
 */
export default {
  name: "UnderConstructionAlert",
};
</script>

<script setup lang="ts">
import Alert from "./Alert.vue";
</script>
