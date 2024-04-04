<template>
  <node-display
    v-if="displayActions"
    variant="menu"
    color="neutral"
    @mousedown.stop
    @mouseup.stop
  >
    <flex-box>
      <icon-button
        tooltip="Create artifact"
        icon="create-artifact"
        data-cy="button-add-artifact"
        @click="
          handleAction(() =>
            artifactSaveStore.openPanel({ isNewArtifact: true })
          )
        "
      />
      <icon-button
        tooltip="Create trace link"
        icon="create-trace"
        data-cy="button-add-trace"
        @click="handleAction(() => traceSaveStore.openPanel())"
      />
      <icon-button
        :tooltip="drawMode ? 'Cancel Draw Mode' : 'Draw Trace Link'"
        :icon="drawMode ? 'cancel' : 'trace'"
        @click="handleAction(() => cyStore.drawMode('toggle'))"
      />
      <separator v-if="displayGenerateActions" vertical class="q-mx-xs" />
      <icon-button
        v-if="displayGenerateActions && ENABLED_FEATURES.GENERATE_SUMMARIES"
        tooltip="Summarize artifacts"
        icon="generate-summaries"
        color="gradient"
        data-cy="button-summarize-artifact"
        @click="
          handleAction(() => appStore.openDetailsPanel('summarizeArtifact'))
        "
      />
      <icon-button
        v-if="displayGenerateActions"
        tooltip="Generate artifacts"
        icon="generate-artifacts"
        color="gradient"
        data-cy="button-generate-artifact"
        @click="
          handleAction(() => appStore.openDetailsPanel('generateArtifact'))
        "
      />
      <icon-button
        v-if="displayGenerateActions"
        tooltip="Generate trace links"
        icon="generate-traces"
        color="gradient"
        data-cy="button-generate-trace"
        @click="handleAction(() => appStore.openDetailsPanel('generateTrace'))"
      />
    </flex-box>
  </node-display>
</template>

<script lang="ts">
/**
 * Renders a context menu for the artifact tree.
 */
export default {
  name: "ArtifactMenu",
};
</script>

<script setup lang="ts">
import { computed, inject } from "vue";
import { ENABLED_FEATURES } from "@/util";
import {
  appStore,
  artifactSaveStore,
  cyStore,
  permissionStore,
  traceSaveStore,
} from "@/hooks";
import { FlexBox, IconButton, Separator } from "@/components/common";
import { NodeDisplay } from "@/components/graph/display";

const handleCloseMenu = inject<() => void>("menu-close");

const drawMode = computed(() => appStore.popups.drawTrace);

const displayActions = computed(() =>
  permissionStore.isAllowed("project.edit_data")
);
const displayGenerateActions = computed(() =>
  permissionStore.isAllowed("project.generate")
);

/**
 * Handles a menu action and closes the menu.
 * @param action - The action to handle.
 */
function handleAction(action: () => void): void {
  action();
  handleCloseMenu?.();
}
</script>
