<template>
  <flex-box align="center">
    <artifact-table-delta-chip :artifact="artifact" />
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
      data-cy="artifact-table-artifact"
    />
  </flex-box>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactModel } from "@/types";
import { warningStore } from "@/hooks";
import { Typography, FlexBox } from "@/components/common";
import ArtifactTableDeltaChip from "./ArtifactTableDeltaChip.vue";

/**
 * Displays the name of a row of artifacts.
 */
export default Vue.extend({
  name: "ArtifactTableRowName",
  components: {
    FlexBox,
    Typography,
    ArtifactTableDeltaChip,
  },
  props: {
    artifact: Object as PropType<ArtifactModel>,
  },
  methods: {
    /**
     * Returns whether the artifact has any warnings.
     * @param item - The artifact to search for
     * @return Whether the artifact has warnings.
     */
    getHasWarnings(item: ArtifactModel): boolean {
      return warningStore.artifactWarnings[item.id]?.length > 0;
    },
  },
});
</script>
