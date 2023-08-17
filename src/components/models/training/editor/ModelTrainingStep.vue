<template>
  <q-timeline-entry
    :color="stepColor"
    :title="stepName"
    :subtitle="stepTimestamp"
  >
    <template #title>
      <flex-box justify="between">
        <typography variant="subtitle" :value="stepName" />
        <chip outlined :color="stepColor" :label="step.status" />
      </flex-box>
    </template>
    <flex-box v-if="step.type === 'document'" t="2" align="center">
      <typography value="Trained on documents:" />
      <chip
        v-for="document in step.documents"
        :key="document.url"
        outlined
        class="q-ma-sm"
        :label="document.name"
      />
    </flex-box>
    <flex-box v-else-if="step.type === 'repository'" t="2" align="center">
      <typography value="Trained on repositories:" />
      <chip
        v-for="repo in step.repositories"
        :key="repo.url"
        outlined
        class="q-ma-sm"
        :label="repo.name"
      />
    </flex-box>
    <flex-box v-else-if="step.type === 'project'" t="2" align="center">
      <typography value="Trained on project data:" />
      <flex-box v-for="project in step.projects" :key="project.id">
        <chip outlined color="primary" class="q-ma-sm" :label="project.name" />
        <chip
          v-for="level in project.levels"
          :key="level.source + level.target"
          outlined
          class="q-ma-sm"
          :label="`${level.source} To ${level.target}`"
        />
      </flex-box>
    </flex-box>
  </q-timeline-entry>
</template>

<script lang="ts">
/**
 * Displays logs of the model's training process.
 */
export default {
  name: "ModelTrainingStep",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { ModelTrainingStepProps } from "@/types";
import { timestampToDisplay } from "@/util";
import { Typography, FlexBox, Chip } from "@/components/common";

const props = defineProps<ModelTrainingStepProps>();

const stepName = computed(
  () =>
    ({
      keywords: "Pre-Training: Keywords",
      document: "Pre-Training: Documents",
      repository: "Intermediate-Training: Repositories",
      project: "Fine-Tuning: Project Data",
    }[props.step.type] || "Training")
);

const stepColor = computed(
  () =>
    ({
      "In Progress": "secondary",
      Completed: "primary",
      Failed: "negative",
    }[props.step.status] || "Training")
);

const stepTimestamp = computed(() => timestampToDisplay(props.step.updatedAt));
</script>
