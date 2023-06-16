<template>
  <panel-card>
    <flex-box align="center" justify="between">
      <div>
        <typography
          ellipsis
          variant="subtitle"
          el="h1"
          :value="name"
          data-cy="text-selected-name"
        />
        <q-tooltip>{{ name }}</q-tooltip>
      </div>
      <attribute-chip
        artifact-type
        :value="type"
        data-cy="text-selected-type"
      />
    </flex-box>

    <separator b="2" />

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
</script>
