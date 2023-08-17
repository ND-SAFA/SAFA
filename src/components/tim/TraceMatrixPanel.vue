<template>
  <details-panel panel="displayTraceMatrix">
    <flex-box v-if="displayActions" b="2">
      <text-button
        text
        label="View Artifacts"
        icon="view-tree"
        @click="handleViewLevel"
      />
    </flex-box>

    <panel-card>
      <flex-box align="center" justify="between" class="overflow-hidden">
        <div class="overflow-hidden" data-cy="text-selected-name">
          <typography variant="caption" value="Parent" />
          <list-item
            clickable
            @click="selectionStore.selectArtifactLevel(targetType)"
          >
            <typography
              ellipsis
              variant="subtitle"
              el="h1"
              class="q-my-none"
              :value="targetType"
            />
            <q-tooltip>{{ targetType }}</q-tooltip>
          </list-item>
          <typography variant="caption" value="Child" />
          <list-item
            clickable
            @click="selectionStore.selectArtifactLevel(sourceType)"
          >
            <typography
              ellipsis
              variant="subtitle"
              el="h1"
              class="q-my-none"
              :value="sourceType"
            />
            <q-tooltip>{{ sourceType }}</q-tooltip>
          </list-item>
        </div>

        <flex-box column>
          <icon :id="targetIcon" size="sm" :color="targetColor" />
          <icon
            class="q-my-xs"
            size="sm"
            :color="generatedCount > 0 ? 'nodeGenerated' : 'nodeDefault'"
            variant="trace"
            :rotate="-90"
          />
          <icon :id="sourceIcon" size="sm" :color="sourceColor" />
        </flex-box>
      </flex-box>

      <separator b="2" t="1" />

      <flex-box>
        <flex-item parts="6">
          <typography variant="caption" value="Total Trace Links" />
          <typography el="p" :value="totalCount" />
          <typography variant="caption" value="Generated Trace Links" />
          <typography el="p" :value="generatedCount" />
          <typography variant="caption" value="Approved Trace Links" />
          <typography el="p" :value="approvedCount" />
        </flex-item>
        <flex-item parts="6">
          <typography variant="caption" value="Trace Coverage" />
          <flex-box align="center">
            <attribute-chip
              :value="traceCoverage.percentage"
              confidence-score
            />
            <typography el="span" :value="traceCoverage.text" l="1" />
          </flex-box>
        </flex-item>
      </flex-box>
    </panel-card>

    <panel-card :title="targetArtifactsLabel">
      <template #title-actions>
        <text-button
          text
          label="View Parents"
          icon="view-tree"
          @click="documentStore.addDocumentOfTypes([targetType])"
        />
      </template>
      <list
        v-if="targetArtifacts.length > 0"
        :scroll-height="300"
        data-cy="list-selected-parent-artifacts"
      >
        <list-item
          v-for="artifact in targetArtifacts"
          :key="artifact.id"
          clickable
          :action-cols="1"
          data-cy="list-selected--parent-artifact-item"
          @click="documentStore.addDocumentOfNeighborhood(artifact)"
        >
          <artifact-body-display display-title :artifact="artifact" />
        </list-item>
      </list>
      <typography
        v-else
        l="1"
        variant="caption"
        value="There are no parent artifacts."
      />
    </panel-card>

    <panel-card :title="sourceArtifactsLabel">
      <template #title-actions>
        <text-button
          text
          label="View Children"
          icon="view-tree"
          @click="documentStore.addDocumentOfTypes([sourceType])"
        />
      </template>
      <list
        v-if="sourceArtifacts.length > 0"
        :scroll-height="300"
        data-cy="list-selected-child-artifacts"
      >
        <list-item
          v-for="artifact in sourceArtifacts"
          :key="artifact.id"
          clickable
          :action-cols="1"
          data-cy="list-selected--child-artifact-item"
          @click="documentStore.addDocumentOfNeighborhood(artifact)"
        >
          <artifact-body-display display-title :artifact="artifact" />
        </list-item>
      </list>
      <typography
        v-else
        l="1"
        variant="caption"
        value="There are no child artifacts."
      />
    </panel-card>
  </details-panel>
</template>

<script lang="ts">
/**
 * Displays trace matrix information.
 */
export default {
  name: "TraceMatrixPanel",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import {
  artifactStore,
  documentStore,
  permissionStore,
  selectionStore,
  subtreeStore,
  timStore,
} from "@/hooks";
import {
  PanelCard,
  Typography,
  TextButton,
  Icon,
  DetailsPanel,
  FlexBox,
  Separator,
  ListItem,
  ArtifactBodyDisplay,
  List,
  FlexItem,
  AttributeChip,
} from "@/components/common";

const displayActions = computed(() => permissionStore.projectAllows("editor"));

const traceMatrix = computed(() => selectionStore.selectedTraceMatrix);

const sourceType = computed(() => traceMatrix.value?.sourceType || "");
const sourceIcon = computed(() => timStore.getTypeIcon(sourceType.value));
const sourceColor = computed(() => timStore.getTypeColor(sourceType.value));

const targetType = computed(() => traceMatrix.value?.targetType || "");
const targetIcon = computed(() => timStore.getTypeIcon(targetType.value));
const targetColor = computed(() => timStore.getTypeColor(targetType.value));

const totalCount = computed(() => {
  const count = traceMatrix.value?.count || 0;

  return count === 1 ? "1 Link" : `${count} Links`;
});

const generatedCount = computed(() => {
  const count = traceMatrix.value?.generatedCount || 0;

  return count === 1 ? "1 Link" : `${count} Links`;
});

const approvedCount = computed(() => {
  const count = traceMatrix.value?.approvedCount || 0;

  return count === 1 ? "1 Link" : `${count} Links`;
});

/**
 * Calculate the percentage of child artifacts of this type
 * that trace to at least one parent artifact of this type.
 */
const traceCoverage = computed(() => {
  const sourceArtifacts = artifactStore.allArtifacts.filter(
    (artifact) => artifact.type === sourceType.value
  );
  const sourceCount = sourceArtifacts.length;
  const traceCount = sourceArtifacts
    .map(({ id }) => subtreeStore.getParents(id))
    .filter((parents) =>
      parents.some(
        (id) => artifactStore.getArtifactById(id)?.type === targetType.value
      )
    ).length;
  const coverage = traceCount / sourceCount;

  return {
    text: `(${traceCount}/${sourceCount})`,
    percentage: coverage,
  };
});

const sourceArtifacts = computed(() =>
  artifactStore.getArtifactsByType(sourceType.value)
);
const sourceArtifactsLabel = computed(() =>
  sourceArtifacts.value.length === 1
    ? "1 Child Artifact"
    : `${sourceArtifacts.value.length} Child Artifacts`
);

const targetArtifacts = computed(() =>
  artifactStore.getArtifactsByType(targetType.value)
);
const targetArtifactsLabel = computed(() =>
  targetArtifacts.value.length === 1
    ? "1 Parent Artifact"
    : `${targetArtifacts.value.length} Parent Artifacts`
);

/**
 * Switches to tree view and highlights this type matrix.
 */
function handleViewLevel(): void {
  if (!traceMatrix.value) return;

  documentStore.addDocumentOfTypes([
    traceMatrix.value.sourceType,
    traceMatrix.value.targetType,
  ]);
}
</script>
