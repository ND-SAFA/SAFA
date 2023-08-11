<template>
  <details-panel panel="displayArtifactLevel" data-cy="panel-artifact-type">
    <flex-box v-if="displayActions" b="2">
      <text-button
        text
        label="View Artifacts"
        icon="view-tree"
        @click="documentStore.addDocumentOfTypes([name])"
      />
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

      <typography variant="caption" value="Details" />
      <typography el="p" :value="countDisplay" />
    </panel-card>

    <panel-card :title="parentLabel">
      <list
        v-if="parentCount > 0"
        :scroll-height="300"
        data-cy="list-selected-parents"
      >
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
      <typography
        v-else
        l="1"
        variant="caption"
        value="There are no parent types."
      />
    </panel-card>

    <panel-card :title="childLabel">
      <list
        v-if="childCount > 0"
        :scroll-height="300"
        data-cy="list-selected-children"
      >
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
      <typography
        v-else
        l="1"
        variant="caption"
        value="There are no child types."
      />
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
  projectStore,
  selectionStore,
  sessionStore,
  appStore,
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
} from "@/components/common";

const displayActions = computed(() =>
  sessionStore.isEditor(projectStore.project)
);

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

const countDisplay = computed(() => {
  const count = artifactLevel.value?.count || 0;

  return count === 1 ? "1 Artifact" : `${count} Artifacts`;
});
</script>
