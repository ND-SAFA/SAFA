<template>
  <v-container style="max-width: 40em">
    <under-construction-alert />
    <typography
      el="p"
      value="Link to any code repositories that would train the model to understand code within this domain. Press enter to save a link."
    />
    <v-combobox filled multiple chips deletable-chips label="Repositories" />
    <v-btn disabled block color="primary"> Start Model Pre-Training </v-btn>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GenerationModelSchema } from "@/types";
import { Typography, UnderConstructionAlert } from "@/components/common";

/**
 * A step for training a model on repositories.
 */
export default Vue.extend({
  name: "ModelRepositoryStep",
  components: { Typography, UnderConstructionAlert },
  props: {
    model: {
      type: Object as PropType<GenerationModelSchema>,
      required: true,
    },
  },
});
</script>
