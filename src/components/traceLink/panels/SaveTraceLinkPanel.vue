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
        label="Parent Artifacts"
        :hidden-artifact-ids="traceSaveStore.hiddenTargetIds"
        :default-hidden-types="traceSaveStore.defaultHiddenTargetTypes"
        data-cy="button-trace-save-target"
      />
      <artifact-input
        v-model="traceSaveStore.sourceIds"
        multiple
        label="Child Artifacts"
        class="q-my-md"
        :hidden-artifact-ids="traceSaveStore.hiddenSourceIds"
        :default-hidden-types="traceSaveStore.defaultHiddenSourceTypes"
        data-cy="button-trace-save-source"
      />

      <expansion-item
        label="Allowed Trace Directions"
        data-cy="panel-trace-directions"
      >
        <type-direction-input
          v-for="type in artifactTypes"
          :key="type.id"
          :artifact-type="type"
        />
      </expansion-item>

      <typography
        v-if="!loading"
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
            :loading="loading"
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
import { computed, ref, watch } from "vue";
import { appStore, timStore, traceApiStore, traceSaveStore } from "@/hooks";
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

const loading = ref(false);

const artifactTypes = computed(() => timStore.artifactTypes);

/**
 * Creates a trace link from the given artifacts.
 */
async function handleSubmit(): Promise<void> {
  loading.value = true;

  await traceApiStore.handleCreateAll();

  loading.value = false;
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
