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

      <flex-box t="2" align="center" v-if="step.type === 'document'">
        <typography value="Trained on documents:" />
        <v-chip
          outlined
          class="ma-1"
          v-for="document in step.documents"
          :key="document.url"
        >
          {{ document.name }}
        </v-chip>
      </flex-box>
      <flex-box t="2" align="center" v-else-if="step.type === 'repository'">
        <typography value="Trained on repositories:" />
        <v-chip
          outlined
          class="ma-1"
          v-for="repo in step.repositories"
          :key="repo.url"
        >
          {{ repo.name }}
        </v-chip>
      </flex-box>
      <flex-box t="2" align="center" v-else-if="step.type === 'project'">
        <typography value="Trained on project data:" />
        <flex-box v-for="project in step.projects" :key="project.id">
          <v-chip outlined color="primary" class="ma-1">
            {{ project.name }}
          </v-chip>
          <v-chip
            outlined
            class="ma-1"
            v-for="level in project.levels"
            :key="level.source + level.target"
          >
            {{ level.source }} To {{ level.target }}
          </v-chip>
        </flex-box>
      </flex-box>
    </v-alert>
  </v-timeline-item>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TrainingStepSchema } from "@/types";
import { Typography, FlexBox } from "@/components/common";

/**
 * Displays logs of the model's training process.
 */
export default Vue.extend({
  name: "ModelTrainingStep",
  components: {
    FlexBox,
    Typography,
  },
  props: {
    step: {
      type: Object as PropType<TrainingStepSchema>,
      required: true,
    },
  },
  computed: {
    /**
     * Returns the name of the given step.
     * @return The step's name.
     */
    stepName(): string {
      return (
        {
          keywords: "Pre-Training: Keywords",
          document: "Pre-Training: Documents",
          repository: "Intermediate-Training: Repositories",
          project: "Fine-Tuning: Project Data",
        }[this.step.type] || "Training"
      );
    },
    /**
     * Returns the color of the given step.
     * @return The step's color.
     */
    stepColor(): string {
      return (
        {
          "In Progress": "secondary",
          Completed: "primary",
          Failed: "error",
        }[this.step.status] || "Training"
      );
    },
    /**
     * Returns the timestamp of the given step.
     * @return The step's timestamp.
     */
    stepTimestamp(): string {
      return "12:00 PM, Oct 31, 2022";
    },
  },
});
</script>

<style scoped lang="scss"></style>
