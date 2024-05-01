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
        @click="handleCheckHealth()"
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
import { computed, onMounted, watch } from "vue";
import { IconVariant, ThemeColor } from "@/types";
import { ENABLED_FEATURES } from "@/util";
import {
  artifactSaveStore,
  artifactStore,
  commentApiStore,
  commentStore,
} from "@/hooks";
import {
  PanelCard,
  Icon,
  Typography,
  Separator,
  FlexBox,
  TextButton,
} from "@/components/common";

const artifact = computed(() =>
  artifactSaveStore.editedArtifact.body
    ? artifactSaveStore.editedArtifact
    : artifactStore.selectedArtifact
);

const artifactHealth = computed(() =>
  commentStore.getHealthChecks(artifact.value?.id || "")
);

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

/**
 * Generates health checks for the current artifact.
 */
function handleCheckHealth(preload?: boolean): void {
  if (!artifact.value) return;

  if (preload && !ENABLED_FEATURES.NASA_ARTIFACT_HEALTH_PRELOAD) return;

  commentApiStore.handleLoadHealthChecks(artifact.value);
}

onMounted(() => handleCheckHealth(true));

watch(
  () => artifact.value,
  () => handleCheckHealth(true)
);
</script>
