<template>
  <flex-box v-if="!uploadedJob" justify="center">
    <q-circular-progress color="primary" indeterminate size="md" />
  </flex-box>
  <list-item
    v-if="!!uploadedJob"
    dense
    :title="uploadedJob.name"
    :subtitle="progress"
    class="q-mt-md"
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

<script lang="ts">
/**
 * A sub-step for displaying an in-progress job during onboarding.
 */
export default {
  name: "JobLoadingSubStep",
};
</script>

<script setup lang="ts">
import { computed, onMounted, watch } from "vue";
import { onboardingStore, useTimeDisplay } from "@/hooks";
import { FlexBox, Icon, ListItem } from "@/components/common";

const uploadedJob = computed(() => onboardingStore.uploadedJob);

const { displayTime, resetTime, stopTime } = useTimeDisplay({
  getStart: () => onboardingStore.uploadedJob?.startedAt || "",
  getEnd: () => onboardingStore.uploadedJob?.completedAt || "",
});

const progress = computed(
  () => `${onboardingStore.uploadProgress} (${displayTime.value})`
);

onMounted(() => resetTime());

watch(
  () => uploadedJob.value,
  () => resetTime()
);

watch(
  () => uploadedJob.value?.status,
  (status) => {
    if (status !== "IN_PROGRESS") stopTime();
  }
);
</script>
