<template>
  <v-container class="elevation-3">
    <CytoscapeController>
      <template v-slot:elements>
        <ArtifactTypeNode
          v-for="artifactPanel in artifactPanels"
          :key="artifactPanel.title"
          :type
        />
        <TypeLink />
      </template>
    </CytoscapeController>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TracePanel } from "@/types";
import { ArtifactPanel } from "@/components";
import ArtifactTypeNode from "./ArtifactTypeNode.vue";

export default Vue.extend({
  props: {
    tracePanels: {
      type: Array as PropType<TracePanel[]>,
      required: true,
    },
    artifactPanels: {
      type: Array as PropType<ArtifactPanel[]>,
      required: true,
    },
  },
  components: {},
});
</script>
