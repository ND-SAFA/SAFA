<template>
  <details-panel panel="health">
    <panel-card borderless title="Generate Health Checks">
      <artifact-type-input
        v-model="artifactTypes"
        class="q-mb-md"
        data-cy="input-document-include-types"
        label="Include Artifact Types"
        multiple
        @blur="handleSaveTypes"
      />
      <artifact-input
        v-model="artifactIds"
        class="q-mb-md"
        data-cy="input-document-artifacts"
        label="Artifacts"
        multiple
      />
      <q-select
        v-model="selectedTasks"
        :options="taskOptions"
        emit-value
        label="Select Health Tasks"
        map-options
        multiple
      />
      <flex-box full-width justify="end" t="3">
        <text-button
          :disabled="!isButtonEnabled"
          color="primary"
          label="Perform Health Checks"
          @click="handlePerformHealthChecks"
        />
      </flex-box>
    </panel-card>
  </details-panel>
</template>

<script lang="ts">
export default {
  name: "HealthPanel",
};
</script>
<script lang="ts" setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { QSelect } from "quasar";
import { appStore, jobApiStore } from "@/hooks";
import {
  DetailsPanel,
  ArtifactInput,
  ArtifactTypeInput,
  PanelCard,
  FlexBox,
  TextButton,
} from "@/components/common";
import { performHealthChecks } from "@/api/endpoints/health-api";
import { HealthTask } from "@/types/api/health-api";

// Component state
const artifactTypes = ref<string[]>([]);
const artifactIds = ref<string[]>([]);
const selectedTasks = ref<HealthTask[]>([]);

const isButtonEnabled = computed(() => {
  return (
    selectedTasks.value.length > 0 &&
    (artifactTypes.value.length > 0 || artifactIds.value.length > 0)
  );
});

const taskOptions = ref<Array<{ label: string; value: HealthTask }>>([
  { label: "Contradiction", value: "contradiction" },
  { label: "Concept Matching", value: "concept_matching" },
  { label: "Concept Extraction", value: "concept_extraction" },
]);

// Clear state when the component goes into view
onMounted(() => {
  // Initialize or clear state here if needed
  artifactTypes.value = [];
  artifactIds.value = [];
});

// Optionally, you can clear the state before the component unmounts
onBeforeUnmount(() => {
  artifactTypes.value = [];
  artifactIds.value = [];
});

function handlePerformHealthChecks() {
  performHealthChecks(
    selectedTasks.value,
    artifactIds.value,
    artifactTypes.value
  );
  appStore.closeSidePanels();
  artifactTypes.value = [];
  artifactIds.value = [];
  selectedTasks.value = [];
}
</script>

<style scoped></style>
