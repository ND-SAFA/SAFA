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
        :loading="commentApiStore.healthLoading"
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

    <q-banner
      v-for="check in artifactHealth"
      :key="check.content"
      dense
      class="show-on-hover-parent"
    >
      <flex-box justify="between">
        <flex-box>
          <separator
            vertical
            :color="check.color"
            r="2"
            class="artifact-check"
          />
          <icon
            size="sm"
            :variant="check.icon"
            :color="check.color"
            class="q-mt-sm"
          />
          <typography
            :value="check.content"
            l="2"
            variant="markdown"
            class="q-mt-sm"
          />
        </flex-box>
        <icon-button
          tooltip="Resolve"
          class="show-on-hover-child"
          icon="comment-resolve"
          @click="handleResolveCheck(check)"
        />
      </flex-box>
      <div class="q-ml-sm q-mt-sm">
        <flex-box v-if="check.artifacts.length > 0" wrap>
          <artifact-chip
            v-for="relatedArtifact in check.artifacts"
            :key="relatedArtifact.id"
            :artifact="relatedArtifact"
            :color="check.color"
          />
        </flex-box>
        <flex-box v-if="check.concepts.length > 0">
          <q-chip
            v-for="concept in check.concepts"
            :key="concept"
            :color="check.color"
            outline
            :icon="getIcon('health-unknown')"
            class="artifact-check-chip"
            clickable
            @click="check.action()"
          >
            <typography :value="concept" wrap color="text" />
          </q-chip>
        </flex-box>
      </div>
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
import { AnyCommentSchema } from "@/types";
import { ENABLED_FEATURES, getIcon } from "@/util";
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
import { ArtifactChip } from "@/components/artifact/display";
import IconButton from "@/components/common/button/IconButton.vue";

const artifact = computed(() =>
  artifactSaveStore.editedArtifact.body
    ? artifactSaveStore.editedArtifact
    : artifactStore.selectedArtifact
);

const artifactHealth = computed(() =>
  commentStore.getHealthChecks(artifact.value?.id || "")
);

/**
 * Generates health checks for the current artifact.
 */
function handleCheckHealth(preload?: boolean): void {
  if (!artifact.value) return;

  if (preload && !ENABLED_FEATURES.NASA_ARTIFACT_HEALTH_PRELOAD) return;

  commentApiStore.handleLoadHealthChecks(artifact.value);
}

/**
 * Resolves a comment, hiding it from the list.
 * @param healthCheck - The health check to resolve.
 */
function handleResolveCheck(healthCheck: AnyCommentSchema) {
  if (!artifact.value) return;

  commentApiStore.handleResolveComment(artifact.value, healthCheck);
}

onMounted(() => handleCheckHealth(true));

watch(
  () => artifact.value,
  () => handleCheckHealth(true)
);
</script>
