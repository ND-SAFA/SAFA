<template>
  <list-item
    :clickable="props.clickable"
    :divider="props.displayDivider"
    class="artifact-display"
    @click="emit('click')"
  >
    <flex-box v-if="props.displayTitle" align="center" justify="between">
      <typography :value="props.artifact.name" />
      <attribute-chip artifact-type :value="artifactType" />
    </flex-box>
    <template #subtitle>
      <typography
        v-if="showSummary"
        variant="expandable"
        :value="props.artifact.summary"
        :default-expanded="props.defaultExpanded"
      />
      <typography
        v-else
        :variant="bodyVariant"
        :value="props.artifact.body"
        :default-expanded="props.defaultExpanded"
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
import { ArtifactListItemProps } from "@/types";
import { isCodeArtifact } from "@/util";
import { typeOptionsStore } from "@/hooks";
import { FlexBox, Typography } from "../content";
import { AttributeChip } from "../chip";
import ListItem from "./ListItem.vue";

const props = defineProps<ArtifactListItemProps>();

const emit = defineEmits<{
  /**
   * Called when clicked.
   */
  (e: "click"): void;
}>();

const artifactType = computed(() =>
  typeOptionsStore.getArtifactTypeDisplay(props.artifact.type)
);

const bodyVariant = computed(() =>
  isCodeArtifact(props.artifact?.name || "") ? "code" : "expandable"
);

const showSummary = computed(() => !!props.artifact?.summary);
</script>
