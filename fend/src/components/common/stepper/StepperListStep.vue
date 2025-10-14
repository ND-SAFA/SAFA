<template>
  <div>
    <typography el="h1" variant="subtitle" :value="props.title" />
    <separator />
    <div v-if="props.loading" class="q-py-md q-mx-auto width-fit">
      <q-circular-progress indeterminate size="lg" />
    </div>
    <typography
      v-if="props.itemCount === 0 && !props.loading && props.emptyMessage"
      variant="small"
      el="p"
      :value="props.emptyMessage"
    />
    <div v-if="!props.loading" class="scrollable-md">
      <slot />
    </div>
  </div>
</template>

<script lang="ts">
/**
 * Presents a list in a stepper workflow for item selection.
 */
export default {
  name: "StepperListStep",
};
</script>

<script setup lang="ts">
import { StepperListStepProps } from "@/types";
import { Typography, Separator } from "@/components/common/display";

const props = defineProps<StepperListStepProps>();
</script>
