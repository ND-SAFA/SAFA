<template>
  <flex-box align="center">
    <v-icon
      v-if="getHasWarnings(artifact)"
      color="secondary"
      data-cy="artifact-table-artifact-warning"
    >
      mdi-hazard-lights
    </v-icon>
    <typography
      l="1"
      :value="artifact.name"
      data-cy="artifact-table-row-name"
    />
  </flex-box>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactSchema } from "@/types";
import { warningStore } from "@/hooks";
import { Typography, FlexBox } from "@/components/common";

/**
 * Displays the name of a row of artifacts.
 */
export default Vue.extend({
  name: "ArtifactTableRowName",
  components: {
    FlexBox,
    Typography,
  },
  props: {
    artifact: Object as PropType<ArtifactSchema>,
  },
  methods: {
    /**
     * Returns whether the artifact has any warnings.
     * @param item - The artifact to search for
     * @return Whether the artifact has warnings.
     */
    getHasWarnings(item: ArtifactSchema): boolean {
      return warningStore.artifactWarnings[item.id]?.length > 0;
    },
  },
});
</script>
