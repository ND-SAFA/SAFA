<template>
  <panel-card
    v-if="ENABLED_FEATURES.NASA_ARTIFACT_HEALTH"
    borderless
    collapsable
    title="Artifact Health"
  >
    <template #title-actions>
      <text-button
        text
        color="primary"
        label="Health"
        icon="health"
        data-cy="button-artifact-health"
        class="q-mr-sm"
        @click="handleCheckHealth"
      />
    </template>
    <typography
      v-if="artifactHealth.length === 0"
      value="There are no active health checks."
    />
    <q-banner v-for="check in artifactHealthDisplay" :key="check.content" dense>
      <flex-box align="center">
        <separator vertical :color="check.color" r="2" style="width: 2px" />
        <icon size="sm" :variant="check.icon" :color="check.color" />
        <typography :value="check.content" l="2" />
      </flex-box>
    </q-banner>
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays artifact health checks.
 */
export default {
  name: "ArtifactHealth",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { AnyCommentSchema, IconVariant, ThemeColor } from "@/types";
import { ENABLED_FEATURES } from "@/util";
import {
  PanelCard,
  Icon,
  Typography,
  Separator,
  FlexBox,
  TextButton,
} from "@/components/common";

const EXAMPLE_HEALTH_COMMENTS: AnyCommentSchema[] = [
  {
    id: "1",
    content: "[Matched concept]",
    userId: "tim@safa.ai",
    status: "active",
    type: "matched_concept",
    createdAt: new Date(Date.now()).toISOString(),
    updatedAt: new Date(Date.now()).toISOString(),
    name: "[Concept]",
  },
  {
    id: "2",
    content: "[Conflicting Requirement]",
    userId: "tim@safa.ai",
    status: "active",
    type: "contradiction",
    createdAt: new Date(Date.now()).toISOString(),
    updatedAt: new Date(Date.now()).toISOString(),
    affectedArtifacts: ["1", "2"],
  },
  {
    id: "3",
    content: "[Multiple Concept]",
    userId: "tim@safa.ai",
    status: "active",
    type: "multi_matched_concept",
    createdAt: new Date(Date.now()).toISOString(),
    updatedAt: new Date(Date.now()).toISOString(),
    concepts: ["[Concept 1]", "[Concept 2]"],
  },
];

const artifactHealth = ref<AnyCommentSchema[]>([]);

const artifactHealthDisplay = computed(() =>
  artifactHealth.value
    .filter((comment) => comment.status !== "resolved")
    .map((health) => ({
      ...health,
      icon: ((): IconVariant => {
        switch (health.type) {
          case "matched_concept":
            return "health";
          case "contradiction":
            return "edit";
          case "multi_matched_concept":
            return "warning";
          default:
            return "flag";
        }
      })(),
      color: ((): ThemeColor => {
        switch (health.type) {
          case "matched_concept":
            return "primary";
          case "contradiction":
            return "negative";
          case "multi_matched_concept":
            return "warning";
          default:
            return "secondary";
        }
      })(),
    }))
);

function handleCheckHealth(): void {
  // TODO
  artifactHealth.value = EXAMPLE_HEALTH_COMMENTS;
}
</script>
