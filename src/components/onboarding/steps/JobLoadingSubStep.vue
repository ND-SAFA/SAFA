<template>
  <flex-box v-if="!uploadedJob" justify="center">
    <q-circular-progress color="primary" indeterminate size="md" />
  </flex-box>
  <list-item
    v-if="!!uploadedJob"
    dense
    :title="uploadedJob.name"
    :subtitle="onboardingStore.uploadProgress"
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
import { computed, onMounted, ref, watch } from "vue";
import { onboardingStore } from "@/hooks";
import { FlexBox, Icon, ListItem } from "@/components/common";

const progress = ref("");
const progressTimer = ref<ReturnType<typeof setTimeout> | undefined>();

const uploadedJob = computed(() => onboardingStore.uploadedJob);

function updateProgress() {
  progress.value = onboardingStore.uploadProgress;

  if (uploadedJob.value?.status !== "IN_PROGRESS") return;

  if (progressTimer.value) clearTimeout(progressTimer.value);

  progressTimer.value = setTimeout(() => updateProgress(), 60 * 1000);
}

onMounted(() => updateProgress());

watch(
  () => uploadedJob.value,
  () => updateProgress()
);
</script>
