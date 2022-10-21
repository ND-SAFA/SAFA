<template>
  <v-container style="max-width: 40em">
    <typography
      el="p"
      value="Select which documents and repositories best fit to your domain. You can also add a new repository by pasting its link and clicking enter."
    />
    <v-combobox filled multiple chips deletable-chips label="Documents" />
    <v-combobox filled multiple chips deletable-chips label="Repositories" />
    <v-btn block color="primary"> Continue Model Pre-Training </v-btn>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GenerationModel } from "@/types";
import { Typography } from "@/components/common";

/**
 * A step for pre-training a model with curated documents and repositories.
 */
export default Vue.extend({
  name: "ModelKeywordsStep",
  components: { Typography },
  props: {
    model: {
      type: Object as PropType<GenerationModel>,
      required: true,
    },
  },
});
</script>
