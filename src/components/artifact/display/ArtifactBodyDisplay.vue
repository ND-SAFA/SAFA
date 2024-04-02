<template>
  <list-item
    dense
    :clickable="props.clickable"
    :divider="props.displayDivider"
    :class="props.fullWidth ? 'full-width' : 'artifact-display'"
    :style="smallWindow ? 'padding: 0px' : undefined"
    @click="emit('click')"
  >
    <artifact-name-display
      v-if="props.displayTitle"
      :artifact="props.artifact"
      display-type
    />
    <template #subtitle>
      <typography
        v-if="showSummary"
        variant="expandable"
        :value="props.artifact.summary"
        :default-expanded="props.defaultExpanded"
        :collapse-length="props.defaultExpanded ? 0 : undefined"
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
import { useScreen } from "@/hooks";
import { Typography, ListItem } from "@/components/common";
import ArtifactNameDisplay from "./ArtifactNameDisplay.vue";

const props = defineProps<ArtifactListItemProps>();

const emit = defineEmits<{
  /**
   * Called when clicked.
   */
  (e: "click"): void;
}>();

const { smallWindow } = useScreen();

const showSummary = computed(() => !!props.artifact?.summary);
const isCode = computed(() => props.artifact.isCode);
const bodyVariant = computed(() => (isCode.value ? "code" : "expandable"));
</script>
