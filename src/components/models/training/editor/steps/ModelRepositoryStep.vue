<template>
  <div>
    <under-construction-alert />
    <typography
      el="p"
      value="Link to any code repositories that would train the model to understand code within this domain. Press enter to save a link."
    />
    <select-input multiple label="Repositories" />
    <text-button
      disabled
      block
      label="Start Model Pre-Training"
      color="primary"
      class="q-mt-sm"
    />
  </div>
</template>

<script lang="ts">
/**
 * A step for training a model on repositories.
 */
export default {
  name: "ModelRepositoryStep",
};
</script>

<script setup lang="ts">
import {
  Typography,
  UnderConstructionAlert,
  TextButton,
  SelectInput,
} from "@/components/common";
</script>
