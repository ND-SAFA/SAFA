<template>
  <flex-box align="center" justify="between" class="overflow-hidden">
    <flex-box column full-width>
      <typography
        v-if="isCode"
        variant="caption"
        :value="codePath"
        ellipsis
        :align="props.align"
        class="full-width"
      />
      <typography
        :align="props.align"
        class="full-width"
        :el="props.isHeader ? 'h1' : undefined"
        :variant="props.isHeader ? 'subtitle' : undefined"
        :value="displayName"
        ellipsis
        :data-cy="props.dataCyName"
      />
      <q-tooltip v-if="props.displayTooltip">
        {{ props.artifact.name }}
      </q-tooltip>
    </flex-box>
    <attribute-chip
      v-if="props.displayType"
      artifact-type
      :value="artifactType"
      :data-cy="props.dataCyType"
    />
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays the name, code path, and type of an artifact.
 */
export default {
  name: "ArtifactNameDisplay",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { ArtifactSchema } from "@/types";
import { timStore } from "@/hooks";
import { FlexBox, Typography } from "../../common/display/content";
import { AttributeChip } from "../../common/display/chip";

const props = defineProps<{
  /**
   * The artifact to display.
   */
  artifact: ArtifactSchema;
  /**
   * Whether to display the artifact type.
   */
  displayType?: boolean;
  /**
   * Whether to display the artifact name in a tooltip.
   */
  displayTooltip?: boolean;
  /**
   * Whether to display the name as a header.
   */
  isHeader?: boolean;
  /**
   * Testing selector for the name.
   */
  dataCyName?: string;
  /**
   * Testing selector for the type.
   */
  dataCyType?: string;
  /**
   * The alignment of the name.
   */
  align?: "center" | "left" | "right";
}>();

const artifactType = computed(() => timStore.getTypeName(props.artifact.type));
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
</script>
