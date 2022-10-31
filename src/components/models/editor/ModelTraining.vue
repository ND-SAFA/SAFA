<template>
  <v-container>
    <v-timeline dense>
      <v-timeline-item color="primary" small>
        <v-card outlined class="pa-2">
          <flex-box justify="space-between" align="center">
            <div>
              <typography el="div" bold value="Pre-Training: Documents" />
              <typography variant="caption" value="12:00 PM, Oct 31, 2022" />
            </div>
            <v-chip color="primary">Completed</v-chip>
          </flex-box>
          <flex-box t="2" align="center">
            <typography value="Trained on documents:" />
            <v-chip outlined class="ma-1">BOSCH Automotive Handbook.pdf</v-chip>
          </flex-box>
        </v-card>
      </v-timeline-item>
      <v-timeline-item color="primary" small>
        <v-card outlined class="pa-2">
          <flex-box justify="space-between" align="center">
            <div>
              <typography
                el="div"
                bold
                value="Intermediate-Training: Repositories"
              />
              <typography variant="caption" value="1:00 PM, Oct 31, 2022" />
            </div>
            <v-chip color="primary">Completed</v-chip>
          </flex-box>
          <flex-box t="2" align="center">
            <typography value="Trained on repositories:" />
            <v-chip outlined class="ma-1">organization/my-project</v-chip>
          </flex-box>
        </v-card>
      </v-timeline-item>
      <v-timeline-item color="secondary" small>
        <v-card outlined class="pa-2">
          <flex-box justify="space-between" align="center">
            <div>
              <typography el="div" bold value="Fine-Tuning: Project Data" />
              <typography variant="caption" value="2:00 PM, Oct 31, 2022" />
            </div>
            <v-chip color="secondary">In Progress</v-chip>
          </flex-box>
          <flex-box t="2" align="center">
            <typography value="Trained on project:" />
            <v-chip outlined class="ma-1">My Project</v-chip>
          </flex-box>
          <flex-box align="center">
            <typography value="Trace matrices:" />
            <v-chip outlined class="ma-1">Designs To Designs</v-chip>
            <v-chip outlined class="ma-1">Designs To Requirements</v-chip>
          </flex-box>
        </v-card>
      </v-timeline-item>
      <v-timeline-item color="primary lighten-3" small>
        <v-btn v-if="!addOpen" block color="primary" @click="addOpen = true">
          Add Model Training
        </v-btn>
        <v-card v-else outlined class="pa-2">
          <v-select filled label="Training Type" :items="trainingOptions" />
          <v-btn block color="primary" @click="addOpen = false">
            Start Model Training
          </v-btn>
        </v-card>
      </v-timeline-item>
    </v-timeline>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GenerationModel } from "@/types";
import { Typography, FlexBox } from "@/components/common";

/**
 * Displays logs of the model's training process,
 * and allows for further model training.
 */
export default Vue.extend({
  name: "ModelTraining",
  components: { FlexBox, Typography },
  props: {
    model: {
      type: Object as PropType<GenerationModel>,
      required: true,
    },
  },
  data() {
    return {
      addOpen: false,
      trainingOptions: [
        "Pre-Training: Documents",
        "Intermediate-Training: Repositories",
        "Fine-Tuning: Project Data",
      ],
    };
  },
  computed: {},
  methods: {},
});
</script>

<style scoped lang="scss"></style>
