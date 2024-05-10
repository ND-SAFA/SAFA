<template>
  <div>
    <panel-card title="Related Context" collapsable borderless>
      <template #title-actions>
        <text-button
          v-if="displayActions"
          text
          small
          label="Parent"
          icon="trace"
          :icon-rotate="-90"
          data-cy="button-artifact-link-parent"
          @click="handleLinkParent"
        />
        <text-button
          v-if="displayActions"
          text
          small
          label="Child"
          icon="trace"
          :icon-rotate="90"
          data-cy="button-artifact-link-child"
          @click="handleLinkChild"
        />
        <q-btn-dropdown
          flat
          auto-close
          dense
          size="sm"
          dropdown-icon=""
          :icon="groupType === 'type' ? getIcon('artifact') : getIcon('trace')"
        >
          <flex-box column>
            <text-button
              label="Type"
              icon="artifact"
              small
              text
              block
              align="start"
              @click="groupType = 'type'"
            />
            <text-button
              label="Hierarchy"
              icon="trace"
              small
              block
              text
              @click="groupType = 'hierarchy'"
            />
          </flex-box>
        </q-btn-dropdown>
      </template>

      <expansion-item
        v-for="artifactType in Object.keys(relatedArtifacts)"
        :key="artifactType"
        :label="artifactType"
        default-opened
      >
        <artifact-list-display
          :data-cy="'list-selected-' + artifactType"
          :artifacts="relatedArtifacts[artifactType]"
          :action-cols="1"
          class="bg-background rounded"
          :item-data-cy="'list-selected-item-' + artifactType"
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
      </expansion-item>

      <typography
        v-if="Object.keys(relatedArtifacts).length === 0"
        l="1"
        variant="caption"
        value="There are no parent artifacts."
      />
    </panel-card>
  </div>
</template>

<script lang="ts">
/**
 * Displays the selected node's parents and children.
 */
export default {
  name: "ArtifactContext",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { ArtifactSchema } from "@/types";
import { getIcon } from "@/util";
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
  FlexBox,
} from "@/components/common";
import ExpansionItem from "@/components/common/display/list/ExpansionItem.vue";
import ArtifactListDisplay from "./ArtifactListDisplay.vue";

const groupType = ref<"type" | "hierarchy">("type");

const displayActions = computed(() =>
  permissionStore.isAllowed("project.edit_data")
);

const artifact = computed(() => artifactStore.selectedArtifact);

const artifactId = computed(() => artifact.value?.id || "");

const relatedArtifacts = computed<Record<string, ArtifactSchema[]>>(() =>
  groupType.value === "type"
    ? (
        subtreeStore
          .getParentsAndChildren(artifactId.value)
          .map((id) => artifactStore.getArtifactById(id))
          .filter((artifact) => !!artifact) as ArtifactSchema[]
      ).reduce<Record<string, ArtifactSchema[]>>(
        (acc, artifact) => ({
          ...acc,
          [artifact.type]: [...(acc[artifact.type] || []), artifact],
        }),
        {}
      )
    : {
        Parents: subtreeStore
          .getParents(artifactId.value)
          .map((id) => artifactStore.getArtifactById(id))
          .filter((artifact) => !!artifact) as ArtifactSchema[],
        Children: subtreeStore
          .getChildren(artifactId.value)
          .map((id) => artifactStore.getArtifactById(id))
          .filter((artifact) => !!artifact) as ArtifactSchema[],
      }
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
