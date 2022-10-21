<template>
  <generic-stepper v-model="step" :steps="steps" minimal hide-continue>
    <template v-slot:items>
      <v-stepper-content step="1">
        <v-container style="max-width: 40em">
          <typography
            el="p"
            value="Enter keywords for the domain that this model should be trained on. Press enter to save a keyword."
          />
          <v-combobox filled multiple chips deletable-chips label="Keywords" />
          <typography
            el="p"
            value="Upload any technical documents that would train the model to understand this domain."
          />
          <generic-file-selector />
          <v-btn block color="primary"> Start Model Pre-Training </v-btn>
        </v-container>
      </v-stepper-content>
      <v-stepper-content step="2">
        <v-container style="max-width: 40em">
          <typography
            el="p"
            value="Select which documents and repositories best fit to your domain. You can also add a new repository by pasting its link and clicking enter."
          />
          <v-combobox filled multiple chips deletable-chips label="Documents" />
          <v-combobox
            filled
            multiple
            chips
            deletable-chips
            label="Repositories"
          />
          <v-btn block color="primary"> Continue Model Pre-Training </v-btn>
        </v-container>
      </v-stepper-content>
      <v-stepper-content step="3">
        <v-container>
          <typography
            el="p"
            value="Train the model on trace links in the current project. Both links that exist and those that do not will inform the model."
          />
          <trace-matrix-creator v-model="matrices" />
          <v-btn block color="primary" class="mt-4"> Train Model </v-btn>
        </v-container>
      </v-stepper-content>
    </template>
  </generic-stepper>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactLevelModel, GenerationModel } from "@/types";
import {
  GenericStepper,
  Typography,
  GenericFileSelector,
} from "@/components/common";
import { TraceMatrixCreator } from "@/components/trace-link";

/**
 * A stepper for training a trace generation model.
 */
export default Vue.extend({
  name: "ModelTrainer",
  components: {
    TraceMatrixCreator,
    GenericFileSelector,
    Typography,
    GenericStepper,
  },
  props: {
    model: {
      type: Object as PropType<GenerationModel>,
      required: true,
    },
  },
  data() {
    return {
      step: 1,
      steps: [
        ["Keywords & Documents", true],
        ["Pre-Training Materials", true],
        ["Model Training", true],
      ],

      matrices: [{ source: "", target: "" }] as ArtifactLevelModel[],
    };
  },
  computed: {},
  methods: {},
});
</script>

<style scoped lang="scss"></style>
