<template>
  <v-timeline-item color="primary lighten-3" small>
    <v-btn v-if="!addOpen" block color="primary" @click="addOpen = true">
      Add Model Training
    </v-btn>
    <v-card v-else outlined class="pa-2">
      <tab-list v-model="tab" :tabs="tabs">
        <v-tab-item key="1">
          <model-document-step :model="model" @submit="handleSubmit" />
        </v-tab-item>
        <v-tab-item key="2">
          <model-repository-step :model="model" @submit="handleSubmit" />
        </v-tab-item>
        <v-tab-item key="3">
          <model-keywords-step :model="model" @submit="handleSubmit" />
        </v-tab-item>
        <v-tab-item key="4">
          <model-project-step :model="model" @submit="handleSubmit" />
        </v-tab-item>
      </tab-list>
    </v-card>
  </v-timeline-item>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GenerationModel } from "@/types";
import { trainingTabOptions } from "@/util";
import TabList from "@/components/common/display/TabList.vue";
import {
  ModelProjectStep,
  ModelDocumentStep,
  ModelRepositoryStep,
  ModelKeywordsStep,
} from "./steps";

/**
 * Displays inputs for training a model.
 */
export default Vue.extend({
  name: "ModelTrainingCreator",
  components: {
    TabList,
    ModelKeywordsStep,
    ModelRepositoryStep,
    ModelDocumentStep,
    ModelProjectStep,
  },
  props: {
    model: {
      type: Object as PropType<GenerationModel>,
      required: true,
    },
  },
  data() {
    return {
      addOpen: false,
      tab: 3,
      tabs: trainingTabOptions(),
    };
  },
  methods: {
    /**
     * Called once a step has been submitted.
     */
    handleSubmit(): void {
      this.addOpen = false;
    },
  },
});
</script>
