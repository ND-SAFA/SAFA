<template>
  <div>
    <model-training :model="model" />
    <!--    <tab-list v-model="tab" :tabs="tabs">-->
    <!--      <v-tab-item key="1">-->
    <!--        <model-training :model="model" />-->
    <!--      </v-tab-item>-->
    <!--      <v-tab-item key="2">-->
    <!--        <under-construction-alert />-->
    <!--      </v-tab-item>-->
    <!--    </tab-list>-->
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GenerationModel } from "@/types";
import { modelEditorTabOptions } from "@/util";
import ModelTraining from "./ModelTraining.vue";

/**
 * Renders model configuration options.
 */
export default Vue.extend({
  name: "ModelEditor",
  components: { ModelTraining },
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
