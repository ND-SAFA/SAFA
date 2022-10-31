<template>
  <v-container style="max-width: 40em">
    <typography
      el="p"
      value="Link to any code repositories that would train the model to understand code within this domain. Press enter to save a link."
    />
    <v-combobox filled multiple chips deletable-chips label="Repositories" />
    <v-btn block color="primary"> Start Model Pre-Training </v-btn>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GenerationModel } from "@/types";
import { Typography } from "@/components/common";

/**
 * A step for training a model on repositories.
 */
export default Vue.extend({
  name: "ModelRepositoryStep",
  components: { Typography },
  props: {
    model: {
      type: Object as PropType<GenerationModel>,
      required: true,
    },
  },
});
</script>
