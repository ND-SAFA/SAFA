<template>
  <div>
    <under-construction-alert />
    <typography
      el="p"
      value="Upload any technical documents that would train the model to understand this domain."
    />
    <file-input />
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
 * A step for training a model on documents.
 */
export default {
  name: "ModelDocumentStep",
};
</script>

<script setup lang="ts">
import {
  Typography,
  FileInput,
  UnderConstructionAlert,
  TextButton,
} from "@/components/common";
</script>
