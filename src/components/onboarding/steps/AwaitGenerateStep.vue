<template>
  <flex-box v-if="!uploadedJob" justify="center">
    <q-circular-progress color="primary" indeterminate size="md" />
  </flex-box>
  <template v-else>
    <typography
      el="p"
      value="
        You will receive an email when the import completes.
        This process takes a less than 10 minutes for a few dozen code files, to around 30 minutes for a few hundred code files.
      "
    />
    <!-- TODO: handle errors with followup call -->
    <list-item
      dense
      :title="uploadedJob.name"
      :subtitle="onboardingStore.uploadProgress"
    >
      <template #icon>
        <q-circular-progress
          v-if="uploadedJob.status === 'IN_PROGRESS'"
          color="gradient"
          indeterminate
          size="md"
        />
        <icon
          v-else-if="uploadedJob.status === 'COMPLETED'"
          variant="job-complete"
          color="primary"
          size="md"
        />
        <icon
          v-else-if="uploadedJob.status === 'FAILED'"
          variant="job-fail"
          color="error"
          size="md"
        />
      </template>
    </list-item>
  </template>
</template>

<script lang="ts">
/**
 *
 */
export default {
  name: "AwaitGenerateStep",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { onboardingStore } from "@/hooks";
import { FlexBox, Icon, ListItem, Typography } from "@/components";

const uploadedJob = computed(() => onboardingStore.uploadedJob);
</script>
