<template>
  <list-item
    subtitle
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
        secondary
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
import { FlexBox } from "@/components/common/layout";
import { ListItem } from "./list";
import { AttributeChip } from "./attribute";
import Typography from "./Typography.vue";

const props = defineProps<{
  artifact: ArtifactSchema;
  displayTitle?: boolean;
  displayDivider?: boolean;
  clickable?: boolean;
}>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const artifactType = computed(() =>
  typeOptionsStore.getArtifactTypeDisplay(props.artifact.type)
);
</script>
