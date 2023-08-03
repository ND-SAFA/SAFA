<template>
  <panel-card>
    <flex-box align="center" justify="between">
      <flex-box column>
        <typography
          v-if="isCode"
          variant="caption"
          :value="codePath"
          el="h1"
          ellipsis
          data-cy="text-selected-name"
        />
        <typography variant="subtitle" :value="displayName" ellipsis />
        <q-tooltip>{{ displayName }}</q-tooltip>
      </flex-box>
      <attribute-chip
        artifact-type
        :value="type"
        data-cy="text-selected-type"
      />
    </flex-box>

    <separator b="2" t="1" />

    <typography variant="caption" value="Body" />
    <typography
      default-expanded
      :variant="variant"
      :value="body"
      data-cy="text-selected-body"
    />

    <artifact-summary />

    <attribute-list-display v-if="!!artifact" :artifact="artifact" />
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays the selected node's title and option buttons.
 */
export default {
  name: "ArtifactFields",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { isCodeArtifact } from "@/util";
import { selectionStore } from "@/hooks";
import {
  Typography,
  FlexBox,
  AttributeChip,
  PanelCard,
  AttributeListDisplay,
  Separator,
} from "@/components/common";
import ArtifactSummary from "./ArtifactSummary.vue";

const artifact = computed(() => selectionStore.selectedArtifact);
const name = computed(() => artifact.value?.name || "");
const type = computed(() => artifact.value?.type || "");
const body = computed(() => artifact.value?.body.trim() || "");
const variant = computed(() =>
  isCodeArtifact(artifact.value?.name || "") ? "code" : "expandable"
);

const isCode = computed(() => isCodeArtifact(name.value));

const codePath = computed(() =>
  isCode.value ? name.value.split("/").slice(0, -1).join("/") : ""
);

const displayName = computed(
  () => (isCode.value && name.value.split("/").pop()) || name.value
);
</script>
