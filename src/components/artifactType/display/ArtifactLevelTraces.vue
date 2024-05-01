<template>
  <div>
    <panel-card
      v-if="parentCount > 0"
      :title="parentLabel"
      collapsable
      borderless
    >
      <list
        :scroll-height="300"
        data-cy="list-selected-parents"
        class="bg-background rounded"
      >
        <list-item
          v-for="parent in parentTypes"
          :key="parent.typeId"
          clickable
          :title="parent.name"
          :icon-id="timStore.getTypeIcon(parent.name)"
          :color="timStore.getTypeColor(parent.color)"
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

    <panel-card
      v-if="childCount > 0"
      :title="childLabel"
      collapsable
      borderless
    >
      <list
        :scroll-height="300"
        data-cy="list-selected-children"
        class="bg-background rounded"
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
    </panel-card>
  </div>
</template>

<script lang="ts">
/**
 * Displays that other artifact levels that the selected artifact type traces to.
 */
export default {
  name: "ArtifactLevelTraces",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { timStore, selectionStore } from "@/hooks";
import { PanelCard, List, ListItem, IconButton } from "@/components/common";

const artifactLevel = computed(() => timStore.selectedArtifactLevel);
const name = computed(() => artifactLevel.value?.name || "");

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
</script>
