<template>
  <div>
    <panel-card :title="parentTitle" collapsable borderless>
      <template #title-actions>
        <text-button
          v-if="displayActions"
          text
          label="Link Parent"
          icon="add"
          data-cy="button-artifact-link-parent"
          @click="handleLinkParent"
        />
      </template>

      <artifact-list-display
        v-if="parents.length > 0"
        data-cy="list-selected-parents"
        :artifacts="parents"
        :action-cols="1"
        item-data-cy="list-selected-parent-item"
        @click="handleArtifactClick($event.name)"
      >
        <template #actions="{ artifact: parent }">
          <icon-button
            outline
            :flat="false"
            icon="trace"
            tooltip="View Trace Link"
            data-cy="button-selected-parent-link"
            :class="getTraceLinkClassName(parent.name)"
            @click="handleTraceLinkClick(parent.name)"
          />
        </template>
      </artifact-list-display>
      <typography
        v-else
        l="1"
        variant="caption"
        value="There are no parent artifacts."
      />
    </panel-card>

    <panel-card :title="childTitle" collapsable borderless>
      <template #title-actions>
        <text-button
          v-if="displayActions"
          text
          label="Link Child"
          icon="add"
          data-cy="button-artifact-link-child"
          @click="handleLinkChild"
        />
      </template>

      <artifact-list-display
        v-if="children.length > 0"
        data-cy="list-selected-children"
        :artifacts="children"
        :action-cols="1"
        item-data-cy="list-selected-child-item"
        @click="handleArtifactClick($event.name)"
      >
        <template #actions="{ artifact: child }">
          <icon-button
            outline
            :flat="false"
            icon="trace"
            tooltip="View Trace Link"
            data-cy="button-selected-child-link"
            :class="getTraceLinkClassName(child.name)"
            @click="handleTraceLinkClick(child.name)"
          />
        </template>
      </artifact-list-display>
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
import { ArtifactSchema } from "@/types";
import {
  artifactStore,
  permissionStore,
  selectionStore,
  subtreeStore,
  traceSaveStore,
  traceStore,
} from "@/hooks";
import {
  Typography,
  IconButton,
  PanelCard,
  TextButton,
} from "@/components/common";
import ArtifactListDisplay from "./ArtifactListDisplay.vue";

const displayActions = computed(() =>
  permissionStore.isAllowed("project.edit_data")
);

const artifact = computed(() => artifactStore.selectedArtifact);

const parents = computed(() =>
  artifact.value
    ? (subtreeStore
        .getParents(artifact.value.id)
        .map((id) => artifactStore.getArtifactById(id))
        .filter((artifact) => !!artifact) as ArtifactSchema[])
    : []
);

const children = computed(() =>
  artifact.value
    ? (subtreeStore
        .getChildren(artifact.value.id)
        .map((id) => artifactStore.getArtifactById(id))
        .filter((artifact) => !!artifact) as ArtifactSchema[])
    : []
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
 * Determines the className of the link to another artifact.
 * @param artifactName - The artifact to select the link to.
 * @returns The className for the link.
 */
function getTraceLinkClassName(artifactName: string): string {
  const relatedArtifact = artifactStore.getArtifactByName(artifactName);

  if (!relatedArtifact || !artifact.value) return "trace-chip text-nodeDefault";

  const traceLink = traceStore.getTraceLinkByArtifacts(
    relatedArtifact.id,
    artifact.value.id,
    true
  );

  const base =
    traceLink?.traceType === "GENERATED"
      ? "trace-chip-generated text-nodeGenerated "
      : "trace-chip text-nodeDefault ";
  const unreviewed =
    traceLink?.approvalStatus === "UNREVIEWED" ? "trace-chip-unreviewed" : "";

  return base + unreviewed;
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

  traceSaveStore.openPanel({
    type: "source",
    artifactId: artifact.value.id,
  });
}

/**
 * Opens the create trace link panel with this artifact as the parent.
 */
function handleLinkChild(): void {
  if (!artifact.value) return;

  traceSaveStore.openPanel({
    type: "target",
    artifactId: artifact.value.id,
  });
}
</script>
