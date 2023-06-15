<template>
  <div v-if="doDisplay">
    <panel-card>
      <text-button
        text
        block
        :label="`View Related Artifacts`"
        icon="view-tree"
        @click="handleViewNeighborhood"
      />
    </panel-card>

    <panel-card :title="parentTitle">
      <template #title-actions>
        <text-button
          text
          label="Link Parent"
          icon="add"
          data-cy="button-artifact-link-parent"
          @click="handleLinkParent"
        />
      </template>
      <list
        v-if="parents.length > 0"
        :scroll-height="300"
        data-cy="list-selected-parents"
      >
        <list-item
          v-for="parent in parents"
          :key="parent.id"
          clickable
          :action-cols="1"
          data-cy="list-selected-parent-item"
          @click="handleArtifactClick(parent.name)"
        >
          <artifact-body-display display-title :artifact="parent" />
          <template #actions>
            <icon-button
              icon="trace"
              tooltip="View Trace Link"
              data-cy="button-selected-parent-link"
              @click="handleTraceLinkClick(parent.name)"
            />
          </template>
        </list-item>
      </list>
      <typography
        v-else
        l="1"
        variant="caption"
        value="There are no parent artifacts."
      />
    </panel-card>

    <panel-card :title="childTitle">
      <template #title-actions>
        <text-button
          text
          label="Link Child"
          icon="add"
          data-cy="button-artifact-link-child"
          @click="handleLinkChild"
        />
      </template>
      <list
        v-if="children.length > 0"
        :scroll-height="300"
        data-cy="list-selected-children"
      >
        <list-item
          v-for="child in children"
          :key="child.id"
          clickable
          :action-cols="1"
          data-cy="list-selected-child-item"
          @click="handleArtifactClick(child.name)"
        >
          <artifact-body-display display-title :artifact="child" />
          <template #actions>
            <icon-button
              icon="trace"
              tooltip="View Trace Link"
              data-cy="button-selected-child-link"
              @click="handleTraceLinkClick(child.name)"
            />
          </template>
        </list-item>
      </list>
      <typography
        v-else
        l="1"
        variant="caption"
        value="There are no child artifacts."
      />
    </panel-card>
  </div>
</template>

<script lang="ts">
/**
 * Displays the selected node's parents and children.
 */
export default {
  name: "ArtifactTraces",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import {
  appStore,
  artifactStore,
  documentStore,
  selectionStore,
  subtreeStore,
  traceStore,
} from "@/hooks";
import {
  Typography,
  IconButton,
  PanelCard,
  ArtifactBodyDisplay,
  TextButton,
  List,
  ListItem,
} from "@/components/common";

const artifact = computed(() => selectionStore.selectedArtifact);

const parents = computed(() =>
  artifact.value
    ? subtreeStore
        .getParents(artifact.value.id)
        .map((id) => artifactStore.getArtifactById(id))
    : []
);

const children = computed(() =>
  artifact.value
    ? subtreeStore
        .getChildren(artifact.value.id)
        .map((id) => artifactStore.getArtifactById(id))
    : []
);

const doDisplay = computed(
  () => parents.value.length + children.value.length > 0
);

const parentTitle = computed(() =>
  parents.value.length === 1
    ? "1 Parent Artifact"
    : `${parents.value.length} Parent Artifacts`
);

const childTitle = computed(() =>
  children.value.length === 1
    ? "1 Child Artifact"
    : `${children.value.length} Child Artifacts`
);

/**
 * Opens a new view with this artifact and all artifacts it traces to.
 */
function handleViewNeighborhood(): void {
  if (!artifact.value) return;

  documentStore.addDocumentOfNeighborhood(artifact.value);
}

/**
 * Selects an artifact.
 * @param artifactName - The artifact to select.
 */
function handleArtifactClick(artifactName: string): void {
  const relatedArtifact = artifactStore.getArtifactByName(artifactName);

  if (!relatedArtifact) return;

  selectionStore.selectArtifact(relatedArtifact.id);
}

/**
 * Selects the trace link to an artifact.
 * @param artifactName - The artifact to select the link to.
 */
function handleTraceLinkClick(artifactName: string): void {
  const relatedArtifact = artifactStore.getArtifactByName(artifactName);

  if (!relatedArtifact || !artifact.value) return;

  const traceLink = traceStore.getTraceLinkByArtifacts(
    relatedArtifact.id,
    artifact.value.id,
    true
  );

  if (!traceLink) return;

  selectionStore.selectTraceLink(traceLink);
}

/**
 * Opens the create trace link panel with this artifact as the child.
 */
function handleLinkParent(): void {
  if (!artifact.value) return;

  appStore.openTraceCreatorTo({
    type: "source",
    artifactId: artifact.value.id,
  });
}

/**
 * Opens the create trace link panel with this artifact as the parent.
 */
function handleLinkChild(): void {
  if (!artifact.value) return;

  appStore.openTraceCreatorTo({
    type: "target",
    artifactId: artifact.value.id,
  });
}
</script>
