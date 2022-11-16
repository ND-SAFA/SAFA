<template>
  <v-container v-if="!generated" style="max-width: 40em">
    <under-construction-alert />
    <typography
      el="p"
      value="Enter keywords for the domain that this model should be trained on. Press enter to save a keyword."
    />
    <v-combobox filled multiple chips deletable-chips label="Keywords" />
    <v-btn block color="primary"> Generate Training Materials </v-btn>
  </v-container>
  <v-container v-else style="max-width: 40em">
    <typography
      el="p"
      value="Select which documents and repositories best fit to your domain. You can also add a new repository by pasting its link and clicking enter."
    />
    <v-combobox filled multiple chips deletable-chips label="Documents" />
    <v-combobox filled multiple chips deletable-chips label="Repositories" />
    <v-btn disabled block color="primary"> Start Model Pre-Training </v-btn>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GenerationModel } from "@/types";
import { Typography, UnderConstructionAlert } from "@/components/common";

/**
 * A step for pre-training a model with keywords and documents.
 */
export default Vue.extend({
  name: "ModelKeywordsStep",
  components: { Typography, UnderConstructionAlert },
  props: {
    model: {
      type: Object as PropType<GenerationModel>,
      required: true,
    },
    generated: Boolean,
  },
});
</script>
