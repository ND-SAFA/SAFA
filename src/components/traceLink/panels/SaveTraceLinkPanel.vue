<template>
  <details-panel
    panel="saveTrace"
    data-cy="panel-trace-save"
    @open="handleOpen"
  >
    <panel-card class="q-mt-md">
      <artifact-input
        v-model="sourceArtifactId"
        label="Source Artifact"
        data-cy="button-trace-save-source"
      />
      <artifact-input
        v-model="targetArtifactId"
        label="Target Artifact"
        class="q-my-md"
        data-cy="button-trace-save-target"
      />

      <expansion-item
        label="Allowed Trace Directions"
        data-cy="panel-trace-directions"
      >
        <type-direction-input
          v-for="level in artifactLevels"
          :key="level.typeId"
          :artifact-level="level"
        />
      </expansion-item>

      <typography
        el="p"
        color="negative"
        class="q-my-md"
        :value="errorMessage"
      />

      <template #actions>
        <flex-box full-width justify="end">
          <text-button
            label="Create"
            icon="save"
            color="primary"
            :disabled="!canSave"
            data-cy="button-trace-save"
            @click="handleSubmit"
          />
        </flex-box>
      </template>
    </panel-card>
  </details-panel>
</template>

<script lang="ts">
/**
 * Allows for creating trace links.
 */
export default {
  name: "SaveTraceLinkPanel",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { appStore, artifactStore, traceStore, typeOptionsStore } from "@/hooks";
import { handleCreateLink } from "@/api";
import {
  Typography,
  ArtifactInput,
  TypeDirectionInput,
  FlexBox,
  ExpansionItem,
  PanelCard,
  TextButton,
} from "@/components/common";
import DetailsPanel from "@/components/navigation/detailsDrawer/DetailsPanel.vue";

const sourceArtifactId = ref("");
const targetArtifactId = ref("");

const sourceArtifact = computed(() =>
  artifactStore.getArtifactById(sourceArtifactId.value)
);
const targetArtifact = computed(() =>
  artifactStore.getArtifactById(targetArtifactId.value)
);

const errorMessage = computed(() => {
  if (!sourceArtifact.value || !targetArtifact.value) return "";

  const isLinkAllowed = traceStore.isLinkAllowed(
    sourceArtifact.value,
    targetArtifact.value
  );

  return isLinkAllowed === true
    ? ""
    : isLinkAllowed || "Cannot create a trace link.";
});

const canSave = computed(
  () =>
    !!sourceArtifactId.value &&
    !!targetArtifactId.value &&
    errorMessage.value === ""
);

const artifactLevels = computed(() => typeOptionsStore.artifactLevels);

/**
 * Resets the panel state.
 */
function handleOpen(): void {
  const openState = appStore.isTraceCreatorOpen;

  sourceArtifactId.value = "";
  targetArtifactId.value = "";

  if (typeof openState !== "object") return;

  if (openState.type === "source") {
    sourceArtifactId.value = openState.artifactId;
  } else if (openState.type === "target") {
    targetArtifactId.value = openState.artifactId;
  } else {
    sourceArtifactId.value = openState.sourceId;
    targetArtifactId.value = openState.targetId;
  }
}

/**
 * Creates a trace link from the given artifacts.
 */
async function handleSubmit(): Promise<void> {
  if (!sourceArtifact.value || !targetArtifact.value) return;

  await handleCreateLink(sourceArtifact.value, targetArtifact.value);

  appStore.closeSidePanels();
}
</script>
