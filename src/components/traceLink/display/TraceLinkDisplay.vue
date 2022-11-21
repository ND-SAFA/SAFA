<template>
  <div>
    <v-row class="my-1" v-if="!showOnly">
      <v-col cols="6">
        <generic-artifact-body-display
          :artifact="sourceArtifact"
          display-title
          display-divider
        />
      </v-col>

      <v-divider vertical inset />

      <v-col cols="6">
        <generic-artifact-body-display
          :artifact="targetArtifact"
          display-title
          display-divider
        />
      </v-col>
    </v-row>

    <typography
      v-else
      defaultExpanded
      secondary
      t="1"
      variant="expandable"
      :value="showOnly === 'source' ? sourceArtifact.body : targetArtifact.body"
    />
  </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactModel, TraceLinkModel } from "@/types";
import { artifactStore } from "@/hooks";
import { Typography, GenericArtifactBodyDisplay } from "@/components/common";

/**
 * Displays a trace link.
 */
export default Vue.extend({
  name: "TraceLinkDisplay",
  components: {
    Typography,
    GenericArtifactBodyDisplay,
  },
  props: {
    link: {
      type: Object as PropType<TraceLinkModel>,
      required: true,
    },
    showOnly: String as PropType<"source" | "target">,
  },
  data() {
    return {
      isSourceExpanded: false,
      isTargetExpanded: false,
    };
  },
  computed: {
    /**
     * @return The artifact this link comes from.
     */
    sourceArtifact(): ArtifactModel | undefined {
      return artifactStore.getArtifactById(this.link.sourceId);
    },
    /**
     * @return The artifact this link goes towards.
     */
    targetArtifact(): ArtifactModel | undefined {
      return artifactStore.getArtifactById(this.link.targetId);
    },
  },
});
</script>
