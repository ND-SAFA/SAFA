<template>
  <v-container class="mt-2">
    <typography el="h1" variant="title" value="Type Options" />
    <v-divider class="mb-2" />
    <div v-for="entry in artifactDirections" :key="entry.type" class="mt-2">
      <typography el="h2" variant="subtitle" :value="entry.label" />
      <v-divider />
      <type-direction-input :entry="entry" />
      <type-icon-input :entry="entry" />
    </div>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { LabelledTraceDirectionModel } from "@/types";
import { typeOptionsModule } from "@/store";
import {
  Typography,
  TypeDirectionInput,
  TypeIconInput,
} from "@/components/common";

/**
 * Renders a tab for changing artifact type icons and trace directions.
 */
export default Vue.extend({
  name: "TypeOptionsTab",
  components: { TypeIconInput, TypeDirectionInput, Typography },
  computed: {
    /**
     * @return The current project's artifact types.
     */
    artifactDirections(): LabelledTraceDirectionModel[] {
      return typeOptionsModule.labeledTypeDirections();
    },
  },
});
</script>
