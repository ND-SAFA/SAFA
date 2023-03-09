<template>
  <list-item
    :clickable="props.clickable"
    :divider="props.displayDivider"
    style="max-width: 500px"
    @click="emit('click')"
  >
    <flex-box align="center" justify="between">
      <typography :value="props.artifact.name" />
      <attribute-chip artifact-type :value="artifactType" />
    </flex-box>
    <template #subtitle>
      <typography
        variant="expandable"
        :value="props.artifact.body"
        :default-expanded="!!props.displayDivider && !!props.displayTitle"
      />
    </template>
  </list-item>
</template>

<script lang="ts">
/**
 * Displays the body of an artifact that can be expanded.
 */
export default {
  name: "ArtifactBodyDisplay",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { ArtifactSchema } from "@/types";
import { typeOptionsStore } from "@/hooks";
import { FlexBox, Typography } from "../content";
import { AttributeChip } from "../chip";
import ListItem from "./ListItem.vue";

const props = defineProps<{
  /**
   * The artifact to display.
   */
  artifact: ArtifactSchema;
  /**
   * Whether to display the title.
   */
  displayTitle?: boolean;
  /**
   * Whether to display a divider between the content.
   */
  displayDivider?: boolean;
  /**
   * Whether the content is clickable.
   */
  clickable?: boolean;
}>();

const emit = defineEmits<{
  /**
   * Called when clicked.
   */
  (e: "click"): void;
}>();

const artifactType = computed(() =>
  typeOptionsStore.getArtifactTypeDisplay(props.artifact.type)
);
</script>
