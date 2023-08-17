<template>
  <details-panel panel="displayArtifactLevel" data-cy="panel-artifact-type">
    <flex-box v-if="displayActions" b="2">
      <text-button
        text
        label="Edit Type"
        icon="edit"
        @click="appStore.openDetailsPanel('saveArtifactLevel')"
      />
    </flex-box>

    <panel-card>
      <flex-box align="center" justify="between">
        <typography
          ellipsis
          variant="subtitle"
          el="h1"
          :value="name"
          data-cy="text-selected-name"
        />
        <q-tooltip>{{ name }}</q-tooltip>
        <icon :id="iconId" size="md" :color="iconColor" />
      </flex-box>

      <separator b="2" />

      <typography variant="caption" value="Artifacts" />
      <typography el="p" :value="artifactCount" />
    </panel-card>

    <panel-card v-if="parentCount > 0" :title="parentLabel">
      <list :scroll-height="300" data-cy="list-selected-parents">
        <list-item
          v-for="parent in parentTypes"
          :key="parent.typeId"
          clickable
          :title="parent.name"
          :icon-id="timStore.getTypeIcon(parent.name)"
          :color="parent.color"
          :action-cols="1"
          data-cy="list-selected-parent-item"
          @click="selectionStore.selectArtifactLevel(parent.name)"
        >
          <template #actions>
            <icon-button
              outline
              :flat="false"
              icon="trace"
              tooltip="View Trace Matrix"
              data-cy="button-selected-parent-link"
              class="trace-chip text-nodeDefault"
              @click="selectionStore.selectTraceMatrix(name, parent.name)"
            />
          </template>
        </list-item>
      </list>
    </panel-card>

    <panel-card v-if="childCount > 0" :title="childLabel">
      <list :scroll-height="300" data-cy="list-selected-children">
        <list-item
          v-for="child in childTypes"
          :key="child.typeId"
          clickable
          :title="child.name"
          :icon-id="timStore.getTypeIcon(child.name)"
          :color="child.color"
          :action-cols="1"
          data-cy="list-selected-child-item"
          @click="selectionStore.selectArtifactLevel(child.name)"
        >
          <template #actions>
            <icon-button
              outline
              :flat="false"
              icon="trace"
              tooltip="View Trace Matrix"
              data-cy="button-selected-child-link"
              class="trace-chip text-nodeDefault"
              @click="selectionStore.selectTraceMatrix(child.name, name)"
            />
          </template>
        </list-item>
      </list>
    </panel-card>

    <panel-card v-if="artifacts.length > 0" :title="artifactsLabel">
      <template #title-actions>
        <text-button
          text
          label="View Artifacts"
          icon="view-tree"
          @click="documentStore.addDocumentOfTypes([name])"
        />
      </template>
      <list :scroll-height="300" data-cy="list-selected-artifacts">
        <list-item
          v-for="artifact in artifacts"
          :key="artifact.id"
          clickable
          :action-cols="1"
          data-cy="list-selected-artifact-item"
          @click="documentStore.addDocumentOfNeighborhood(artifact)"
        >
          <artifact-body-display display-title :artifact="artifact" />
        </list-item>
      </list>
    </panel-card>
  </details-panel>
</template>

<script lang="ts">
/**
 * Displays artifact level information.
 */
export default {
  name: "ArtifactLevelPanel",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import {
  timStore,
  documentStore,
  selectionStore,
  appStore,
  permissionStore,
  artifactStore,
} from "@/hooks";
import {
  PanelCard,
  Typography,
  Icon,
  DetailsPanel,
  FlexBox,
  TextButton,
  Separator,
  List,
  ListItem,
  IconButton,
  ArtifactBodyDisplay,
} from "@/components/common";

const displayActions = computed(() => permissionStore.projectAllows("editor"));

const artifactLevel = computed(() => selectionStore.selectedArtifactLevel);
const name = computed(() => artifactLevel.value?.name || "");
const iconId = computed(() => timStore.getTypeIcon(name.value));
const iconColor = computed(() => timStore.getTypeColor(name.value));

const parentTypes = computed(() => timStore.getParentMatrices(name.value));
const parentCount = computed(() => parentTypes.value?.length || 0);
const parentLabel = computed(() =>
  parentCount.value === 1
    ? "1 Parent Type"
    : `${parentCount.value} Parent Types`
);

const childTypes = computed(() => timStore.getChildMatrices(name.value));
const childCount = computed(() => childTypes.value?.length || 0);
const childLabel = computed(() =>
  childCount.value === 1 ? "1 Child Type" : `${childCount.value} Child Types`
);

const artifactCount = computed(() => artifactLevel.value?.count || 0);

const artifacts = computed(() => artifactStore.getArtifactsByType(name.value));
const artifactsLabel = computed(() =>
  artifacts.value.length === 1
    ? "1 Artifact"
    : `${artifacts.value.length} Artifacts`
);
</script>
