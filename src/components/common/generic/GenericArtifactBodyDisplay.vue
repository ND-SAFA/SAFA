<template>
  <v-list-item-content style="max-width: 500px">
    <v-list-item-title v-if="!!displayTitle">
      <div class="d-flex align-center">
        <span class="text-h6 mr-2">{{ artifact.name }}</span>
        <span class="text-caption text--secondary">{{ artifactType }}</span>
        <v-spacer />
        <v-btn text small @click.stop="isExpanded = !isExpanded">
          {{ isExpanded ? "See Less" : "See More" }}
        </v-btn>
      </div>
      <v-divider v-if="displayDivider || isExpanded" />
    </v-list-item-title>
    <v-list-item-subtitle v-if="!isExpanded" v-html="artifact.body" />
    <v-list-item-content v-if="isExpanded" v-html="artifact.body" />
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
    displayDivider: Boolean,
  },
  data() {
    return {
      isExpanded: this.displayDivider && this.artifact.body.length < 500,
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
