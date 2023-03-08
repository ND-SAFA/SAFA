<template>
  <alert-card
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
import AlertCard from "./AlertCard.vue";
</script>
