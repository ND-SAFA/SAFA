<template>
  <v-list-item-content style="max-width: 500px">
    <v-list-item-title v-if="!!displayTitle">
      <flex-box align="center" justify="space-between">
        <typography :value="artifact.name" />
        <attribute-chip artifact-type :value="artifactType" />
      </flex-box>
      <v-divider class="mt-1" v-if="!!displayDivider" />
    </v-list-item-title>
    <v-list-item-subtitle>
      <typography
        secondary
        variant="expandable"
        :value="artifact.body"
        :defaultExpanded="!!displayDivider && !!displayTitle"
      />
    </v-list-item-subtitle>
  </v-list-item-content>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactModel } from "@/types";
import { typeOptionsStore } from "@/hooks";
import { Typography, FlexBox } from "@/components/common/display";
import AttributeChip from "@/components/common/display/AttributeChip.vue";

/**
 * Displays the body of an artifact that can be expanded.
 */
export default Vue.extend({
  name: "GenericArtifactBodyDisplay",
  components: { AttributeChip, FlexBox, Typography },
  props: {
    artifact: {
      type: Object as PropType<ArtifactModel>,
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
      return typeOptionsStore.getArtifactTypeDisplay(this.artifact.type);
    },
  },
});
</script>
