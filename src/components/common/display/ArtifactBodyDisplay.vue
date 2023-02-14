<template>
  <v-list-item-content style="max-width: 500px">
    <v-list-item-title v-if="!!displayTitle">
      <flex-box align="center" justify="space-between">
        <typography :value="artifact.name" />
        <attribute-chip artifact-type :value="artifactType" />
      </flex-box>
      <v-divider v-if="!!displayDivider" class="mt-1" />
    </v-list-item-title>
    <v-list-item-subtitle>
      <typography
        secondary
        variant="expandable"
        :value="artifact.body"
        :default-expanded="!!displayDivider && !!displayTitle"
      />
    </v-list-item-subtitle>
  </v-list-item-content>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { ArtifactSchema } from "@/types";
import { typeOptionsStore } from "@/hooks";
import { FlexBox } from "@/components/common/layout";
import { AttributeChip } from "./attribute";
import Typography from "./Typography.vue";

/**
 * Displays the body of an artifact that can be expanded.
 */
export default defineComponent({
  name: "ArtifactBodyDisplay",
  components: { AttributeChip, FlexBox, Typography },
  props: {
    artifact: {
      type: Object as PropType<ArtifactSchema>,
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
