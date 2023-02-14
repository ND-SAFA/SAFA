<template>
  <div>
    <v-row v-if="!showOnly" class="my-1">
      <v-col cols="6">
        <artifact-body-display
          :artifact="sourceArtifact"
          display-title
          display-divider
        />
      </v-col>

      <v-divider vertical inset />

      <v-col cols="6">
        <artifact-body-display
          :artifact="targetArtifact"
          display-title
          display-divider
        />
      </v-col>
    </v-row>

    <typography
      v-else
      default-expanded
      secondary
      t="1"
      variant="expandable"
      :value="showOnly === 'source' ? sourceArtifact.body : targetArtifact.body"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { ArtifactSchema, TraceLinkSchema } from "@/types";
import { artifactStore } from "@/hooks";
import { Typography, ArtifactBodyDisplay } from "@/components/common";

/**
 * Displays a trace link.
 */
export default defineComponent({
  name: "TraceLinkDisplay",
  components: {
    Typography,
    ArtifactBodyDisplay,
  },
  props: {
    link: {
      type: Object as PropType<TraceLinkSchema>,
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
    sourceArtifact(): ArtifactSchema | undefined {
      return artifactStore.getArtifactById(this.link.sourceId);
    },
    /**
     * @return The artifact this link goes towards.
     */
    targetArtifact(): ArtifactSchema | undefined {
      return artifactStore.getArtifactById(this.link.targetId);
    },
  },
});
</script>
