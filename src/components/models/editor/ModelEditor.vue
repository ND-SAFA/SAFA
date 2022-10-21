<template>
  <v-container>
    <tab-list v-model="tab" :tabs="tabs">
      <v-tab-item key="1">
        <model-trainer :model="model" />
      </v-tab-item>
      <v-tab-item key="2">
        <model-logs :model="model" />
      </v-tab-item>
      <v-tab-item key="3">
        <under-construction-alert />
      </v-tab-item>
    </tab-list>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GenerationModel } from "@/types";
import { modelEditorTabOptions } from "@/util";
import { TabList, UnderConstructionAlert } from "@/components/common";
import ModelTrainer from "./ModelTrainer.vue";
import ModelLogs from "./ModelLogs.vue";

/**
 * Renders model configuration options.
 */
export default Vue.extend({
  name: "ModelEditor",
  components: { ModelLogs, ModelTrainer, UnderConstructionAlert, TabList },
  props: {
    model: {
      type: Object as PropType<GenerationModel>,
      required: true,
    },
  },
  data() {
    return {
      tab: 0,
      tabs: modelEditorTabOptions(),
    };
  },
  computed: {},
  methods: {},
});
</script>
