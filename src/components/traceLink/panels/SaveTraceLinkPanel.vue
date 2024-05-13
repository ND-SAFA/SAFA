<template>
  <details-panel panel="saveTrace" data-cy="panel-trace-save">
    <panel-card title="Save Trace Link" borderless>
      <artifact-input
        v-model="traceSaveStore.targetIds"
        multiple
        label="Parent Artifacts"
        :hidden-artifact-ids="traceSaveStore.hiddenTargetIds"
        :default-hidden-types="traceSaveStore.defaultHiddenTargetTypes"
        data-cy="button-trace-save-target"
      >
        <template v-if="!!sourceArtifact" #before-options>
          <typography variant="caption" value="Child Artifact" l="2" />
          <separator class="q-mx-sm" />
          <artifact-body-display display-title :artifact="sourceArtifact" />
          <typography variant="caption" value="Parent Artifacts" l="2" />
          <separator class="q-mx-sm" />
        </template>
      </artifact-input>
      <artifact-input
        v-model="traceSaveStore.sourceIds"
        multiple
        label="Child Artifacts"
        class="q-my-md"
        :hidden-artifact-ids="traceSaveStore.hiddenSourceIds"
        :default-hidden-types="traceSaveStore.defaultHiddenSourceTypes"
        data-cy="button-trace-save-source"
      >
        <template v-if="!!targetArtifact" #before-options>
          <typography variant="caption" value="Parent Artifact" l="2" />
          <artifact-body-display display-title :artifact="targetArtifact" />
          <typography variant="caption" value="Child Artifacts" l="2" />
        </template>
      </artifact-input>
      <text-input
        v-model="traceSaveStore.explanation"
        label="Explanation"
        class="q-my-md"
        type="textarea"
        data-cy="input-trace-explanation"
      />

      <expansion-item
        label="Allowed Trace Directions"
        data-cy="panel-trace-directions"
      >
        <type-direction-input
          v-for="type in artifactTypes"
          :key="type.typeId"
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
import { computed, ref } from "vue";
import {
  timStore,
  appStore,
  artifactStore,
  traceApiStore,
  traceSaveStore,
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
  Separator,
} from "@/components/common";
import { ArtifactBodyDisplay } from "@/components/artifact/display";
import TextInput from "@/components/common/input/TextInput.vue";

const loading = ref(false);

const artifactTypes = computed(() => timStore.artifactTypes);

const sourceArtifact = computed(() =>
  traceSaveStore.sourceIds
    ? artifactStore.getArtifactById(traceSaveStore.sourceIds[0])
    : undefined
);
const targetArtifact = computed(() =>
  traceSaveStore.targetIds
    ? artifactStore.getArtifactById(traceSaveStore.targetIds[0])
    : undefined
);

/**
 * Creates a trace link from the given artifacts.
 */
async function handleSubmit(): Promise<void> {
  loading.value = true;

  await traceApiStore.handleCreateAll();

  loading.value = false;
  appStore.closeSidePanels();
  traceSaveStore.resetTrace();
}
</script>
