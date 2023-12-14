<template>
  <panel-card :title="props.hideTitle ? undefined : 'Project Summary'">
    <div
      v-if="!editMode"
      class="overflow-auto"
      :style="hideOverflow ? 'max-height: 40vh' : ''"
    >
      <typography
        v-if="!!specification && displayDescription"
        variant="caption"
        value="Description"
      />
      <typography
        v-if="displayDescription"
        ep="p"
        variant="expandable"
        :value="description"
        default-expanded
        :collapse-length="0"
      />
      <typography
        v-if="!!specification && displayDescription"
        variant="caption"
        value="Specification"
      />
      <typography
        v-if="!!specification"
        ep="p"
        variant="expandable"
        :value="specification"
        default-expanded
        :collapse-length="0"
      />
    </div>
    <text-input
      v-else
      v-model="editedIdentifier.specification"
      type="textarea"
      :rows="20"
      label="Specification"
    />
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays the project description.
 */
export default {
  name: "ProjectOverviewDisplay",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { appStore, identifierSaveStore, projectStore } from "@/hooks";
import { PanelCard, Typography } from "@/components/common";
import TextInput from "@/components/common/input/TextInput.vue";

const props = defineProps<{ hideTitle?: boolean; hideOverflow?: boolean }>();

const editMode = computed(() => appStore.popups.editProject);
const editedIdentifier = computed(() => identifierSaveStore.editedIdentifier);

// Hide the description if it is just a copy of the generated specification.
const displayDescription = computed(
  () =>
    projectStore.project.description.length !==
    projectStore.project.specification?.length
);

const description = computed(
  () => projectStore.project.description || "No Description."
);

const specification = computed(() => projectStore.project.specification);
</script>
