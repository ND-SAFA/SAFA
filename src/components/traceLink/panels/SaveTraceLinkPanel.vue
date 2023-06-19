<template>
  <details-panel
    panel="saveTrace"
    data-cy="panel-trace-save"
    @open="traceSaveStore.resetTrace"
  >
    <panel-card>
      <artifact-input
        v-model="traceSaveStore.targetIds"
        multiple
        label="Target Artifacts"
        :default-hidden-types="traceSaveStore.defaultHiddenTargetTypes"
        data-cy="button-trace-save-target"
      />
      <artifact-input
        v-model="traceSaveStore.sourceIds"
        multiple
        label="Source Artifacts"
        class="q-my-md"
        :default-hidden-types="traceSaveStore.defaultHiddenSourceTypes"
        data-cy="button-trace-save-source"
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
        :value="traceSaveStore.errorMessage"
      />

      <template #actions>
        <flex-box full-width justify="end">
          <text-button
            label="Create"
            icon="save"
            color="primary"
            :disabled="!traceSaveStore.canSave"
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
import { computed, watch } from "vue";
import {
  appStore,
  traceApiStore,
  traceSaveStore,
  typeOptionsStore,
} from "@/hooks";
import {
  Typography,
  ArtifactInput,
  TypeDirectionInput,
  FlexBox,
  ExpansionItem,
  PanelCard,
  TextButton,
  DetailsPanel,
} from "@/components/common";

const artifactLevels = computed(() => typeOptionsStore.artifactLevels);

/**
 * Creates a trace link from the given artifacts.
 */
async function handleSubmit(): Promise<void> {
  await traceApiStore.handleCreateAll();

  appStore.closeSidePanels();
}

watch(
  () => appStore.isTraceCreatorOpen,
  (open) => {
    if (!open) return;

    traceSaveStore.resetTrace();
  }
);
</script>
