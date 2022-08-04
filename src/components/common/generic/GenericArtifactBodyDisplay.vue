<template>
  <v-list-item-content style="max-width: 500px">
    <v-list-item-title v-if="!!displayTitle">
      <div>
        <span class="text-h6 mr-2">{{ artifact.name }}</span>
        <span class="text-caption text--secondary">{{ artifactType }}</span>
      </div>
      <v-divider />
    </v-list-item-title>
    <v-list-item-subtitle v-if="!isExpanded" v-html="artifact.body" />
    <v-list-item-content v-if="isExpanded" v-html="artifact.body" />
    <v-list-item-action class="ma-0 pt-1">
      <v-spacer />
      <v-btn text small @click.stop="isExpanded = !isExpanded">
        {{ isExpanded ? "See Less" : "See More" }}
      </v-btn>
    </v-list-item-action>
  </v-list-item-content>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { Artifact } from "@/types";
import { getArtifactTypePrintName } from "@/util";

/**
 * Displays the body of an artifact that can be expanded.
 */
export default Vue.extend({
  name: "GenericArtifactBodyDisplay",
  props: {
    artifact: {
      type: Object as PropType<Artifact>,
      required: true,
    },
    displayTitle: Boolean,
  },
  data() {
    return {
      isExpanded: false,
    };
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
