<template>
  <v-list-item-content style="max-width: 500px">
    <v-list-item-title v-if="!!displayTitle">
      <div class="d-flex align-center">
        <typography r="2" :value="artifact.name" />
        <typography variant="caption" :value="artifactType" />
      </div>
      <v-divider v-if="!!displayDivider" />
    </v-list-item-title>
    <v-list-item-subtitle>
      <typography
        variant="expandable"
        :value="artifact.body"
        :defaultExpanded="!!displayDivider && !!displayTitle"
      />
    </v-list-item-subtitle>
  </v-list-item-content>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Artifact } from "@/types";
import { getArtifactTypePrintName } from "@/util";
import { Typography } from "@/components/common/display";

/**
 * Displays the body of an artifact that can be expanded.
 */
export default Vue.extend({
  name: "GenericArtifactBodyDisplay",
  components: { Typography },
  props: {
    artifact: {
      type: Object as PropType<Artifact>,
      required: true,
    },
    displayTitle: Boolean,
    displayDivider: Boolean,
  },
  computed: {
    /**
     * Returns the display name for the artifact type.
     */
    artifactType(): string {
      return getArtifactTypePrintName(this.artifact.type);
    },
  },
});
</script>
