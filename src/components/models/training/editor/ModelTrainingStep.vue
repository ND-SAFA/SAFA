<template>
  <q-timeline-entry
    :color="stepColor"
    :title="stepName"
    :subtitle="stepTimestamp"
  >
    <template #title>
      <flex-box justify="between">
        <typography variant="subtitle" :value="stepName" />
        <q-chip outline :color="stepColor">{{ step.status }}</q-chip>
      </flex-box>
    </template>
    <flex-box v-if="step.type === 'document'" t="2" align="center">
      <typography value="Trained on documents:" />
      <q-chip
        v-for="document in step.documents"
        :key="document.url"
        outline
        class="q-ma-sm"
      >
        {{ document.name }}
      </q-chip>
    </flex-box>
    <flex-box v-else-if="step.type === 'repository'" t="2" align="center">
      <typography value="Trained on repositories:" />
      <q-chip
        v-for="repo in step.repositories"
        :key="repo.url"
        outline
        class="q-ma-sm"
      >
        {{ repo.name }}
      </q-chip>
    </flex-box>
    <flex-box v-else-if="step.type === 'project'" t="2" align="center">
      <typography value="Trained on project data:" />
      <flex-box v-for="project in step.projects" :key="project.id">
        <q-chip outline color="primary" class="q-ma-sm">
          {{ project.name }}
        </q-chip>
        <q-chip
          v-for="level in project.levels"
          :key="level.source + level.target"
          outline
          class="q-ma-sm"
        >
          {{ level.source }} To {{ level.target }}
        </q-chip>
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
import { TrainingStepSchema } from "@/types";
import { timestampToDisplay } from "@/util";
import { Typography, FlexBox } from "@/components/common";

const props = defineProps<{
  step: TrainingStepSchema;
}>();

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
