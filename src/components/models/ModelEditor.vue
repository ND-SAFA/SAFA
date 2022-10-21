<template>
  <tab-list v-model="tab" :tabs="tabs">
    <v-tab-item key="1">
      <under-construction-alert />
    </v-tab-item>
    <v-tab-item key="2">
      <under-construction-alert />
    </v-tab-item>
    <v-tab-item key="3">
      <under-construction-alert />
    </v-tab-item>
  </tab-list>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TrainedModel } from "@/types";
import { modelEditorTabOptions } from "@/util";
import { TabList, UnderConstructionAlert } from "@/components/common";

/**
 * Renders model configuration options.
 */
export default Vue.extend({
  name: "ModelEditor",
  components: { UnderConstructionAlert, TabList },
  props: {
    model: {
      type: Object as PropType<TrainedModel>,
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
