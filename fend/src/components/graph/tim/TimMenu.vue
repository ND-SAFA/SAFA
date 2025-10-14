<template>
  <node-display
    v-if="displayActions"
    color="neutral"
    variant="menu"
    @mousedown.stop
    @mouseup.stop
  >
    <flex-box>
      <icon-button
        :icon="drawMode ? 'cancel' : 'trace'"
        :tooltip="
          drawMode ? 'Cancel draw mode' : 'Draw artifact type direction'
        "
        @click="handleAction(() => cyStore.drawMode('toggle'))"
      />
      <separator v-if="displayGenerateActions" class="q-mx-xs" vertical />
      <icon-button
        v-if="displayGenerateActions && ENABLED_FEATURES.GENERATE_SUMMARIES"
        color="gradient"
        data-cy="button-summarize-artifact"
        icon="generate-summaries"
        tooltip="Summarize artifacts"
        @click="
          handleAction(() => appStore.openDetailsPanel('summarizeArtifact'))
        "
      />
      <icon-button
        v-if="displayGenerateActions"
        color="gradient"
        icon="generate-artifacts"
        tooltip="Generate artifacts"
        @click="
          handleAction(() => appStore.openDetailsPanel('generateArtifact'))
        "
      />
      <icon-button
        v-if="displayGenerateActions"
        color="gradient"
        icon="generate-traces"
        tooltip="Generate trace links"
        @click="handleAction(() => appStore.openDetailsPanel('generateTrace'))"
      />
    </flex-box>
  </node-display>
</template>

<script lang="ts">
/**
 * Renders a context menu for the tim tree.
 */
export default {
  name: "TimMenu",
};
</script>

<script lang="ts" setup>
import { computed, inject } from "vue";
import { ENABLED_FEATURES } from "@/util";
import { appStore, cyStore, permissionStore } from "@/hooks";
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
