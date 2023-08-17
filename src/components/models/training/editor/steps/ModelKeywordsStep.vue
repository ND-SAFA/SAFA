<template>
  <div v-if="props.generated">
    <under-construction-alert />
    <typography
      el="p"
      value="Enter keywords for the domain that this model should be trained on. Press enter to save a keyword."
    />
    <select-input multiple label="Keywords" class="q-mb-md" />
    <text-button block label="Generate Training Materials" color="primary" />
  </div>
  <div v-else>
    <under-construction-alert />
    <typography
      el="p"
      value="Select which documents and repositories best fit to your domain. You can also add a new repository by pasting its link and clicking enter."
    />
    <select-input multiple label="Documents" class="q-mb-md" />
    <select-input multiple label="Repositories" class="q-mb-md" />
    <text-button
      disabled
      block
      label="Start Model Pre-Training"
      color="primary"
    />
  </div>
</template>

<script lang="ts">
/**
 * A step for pre-training a model with keywords and documents.
 */
export default {
  name: "ModelKeywordsStep",
};
</script>

<script setup lang="ts">
import { GenerationModelProps } from "@/types";
import {
  Typography,
  SelectInput,
  UnderConstructionAlert,
  TextButton,
} from "@/components/common";

const props = defineProps<GenerationModelProps>();
</script>
