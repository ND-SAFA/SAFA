<template>
  <v-timeline-item small :color="stepColor">
    <v-alert outlined border="left" :color="stepColor">
      <flex-box justify="space-between" align="center">
        <div>
          <typography el="div" bold :value="stepName" />
          <typography variant="caption" :value="stepTimestamp" />
        </div>
        <v-chip :color="stepColor">{{ step.status }}</v-chip>
      </flex-box>

      <flex-box v-if="step.type === 'document'" t="2" align="center">
        <typography value="Trained on documents:" />
        <v-chip
          v-for="document in step.documents"
          :key="document.url"
          outlined
          class="ma-1"
        >
          {{ document.name }}
        </v-chip>
      </flex-box>
      <flex-box v-else-if="step.type === 'repository'" t="2" align="center">
        <typography value="Trained on repositories:" />
        <v-chip
          v-for="repo in step.repositories"
          :key="repo.url"
          outlined
          class="ma-1"
        >
          {{ repo.name }}
        </v-chip>
      </flex-box>
      <flex-box v-else-if="step.type === 'project'" t="2" align="center">
        <typography value="Trained on project data:" />
        <flex-box v-for="project in step.projects" :key="project.id">
          <v-chip outlined color="primary" class="ma-1">
            {{ project.name }}
          </v-chip>
          <v-chip
            v-for="level in project.levels"
            :key="level.source + level.target"
            outlined
            class="ma-1"
          >
            {{ level.source }} To {{ level.target }}
          </v-chip>
        </flex-box>
      </flex-box>
    </v-alert>
  </v-timeline-item>
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
import { defineProps, computed } from "vue";
import { TrainingStepSchema } from "@/types";
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
      Failed: "error",
    }[props.step.status] || "Training")
);

const stepTimestamp = computed(() => "12:00 PM, Jan 1, 2023");
</script>
