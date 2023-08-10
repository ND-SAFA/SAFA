<template>
  <list-item
    dense
    :clickable="props.clickable"
    :divider="props.displayDivider"
    :class="props.fullWidth ? 'full-width' : 'artifact-display'"
    @click="emit('click')"
  >
    <flex-box v-if="props.displayTitle" align="center" justify="between">
      <flex-box column>
        <typography
          v-if="isCode"
          variant="caption"
          :value="codePath"
          ellipsis
        />
        <typography :value="displayName" ellipsis />
      </flex-box>
      <attribute-chip artifact-type :value="artifactType" />
    </flex-box>
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
import { timStore } from "@/hooks";
import { FlexBox, Typography } from "../../common/display/content";
import { AttributeChip } from "../../common/display/chip";
import ListItem from "../../common/display/list/ListItem.vue";

const props = defineProps<ArtifactListItemProps>();

const emit = defineEmits<{
  /**
   * Called when clicked.
   */
  (e: "click"): void;
}>();

const artifactType = computed(() => timStore.getTypeName(props.artifact.type));
const showSummary = computed(() => !!props.artifact?.summary);
const isCode = computed(() => props.artifact.isCode);

const codePath = computed(() =>
  isCode.value
    ? props.artifact.name.split("/").slice(0, -1).join("/")
    : undefined
);

const displayName = computed(
  () =>
    (isCode.value && props.artifact.name.split("/").pop()) ||
    props.artifact.name
);

const bodyVariant = computed(() => (isCode.value ? "code" : "expandable"));
</script>
