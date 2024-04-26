<template>
  <panel-card
    :title="props.hideTitle ? undefined : name"
    :borderless="props.borderless"
  >
    <template v-if="!props.hideTitle" #title-actions>
      <typography secondary :value="versionLabel" />
    </template>
    <div class="overflow-auto" :style="hideOverflow ? 'max-height: 40vh' : ''">
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
        copyable
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
        copyable
      />
    </div>
    <!--    <text-input-->
    <!--      v-else-->
    <!--      v-model="editedIdentifier.specification"-->
    <!--      disabled-->
    <!--      type="textarea"-->
    <!--      :rows="4"-->
    <!--      label="Specification"-->
    <!--    />-->
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
import { versionToString } from "@/util";
import { projectStore } from "@/hooks";
import { PanelCard, Typography } from "@/components/common";

const props = defineProps<{
  hideTitle?: boolean;
  hideOverflow?: boolean;
  borderless?: boolean;
}>();

// const editMode = computed(() => appStore.popups.editProject);
// const editedIdentifier = computed(() => identifierSaveStore.editedIdentifier);

const displayDescription = computed(
  () =>
    // If there is no specification, show the description.
    !projectStore.project.specification &&
    // If the description is the same as the specification, hide it.
    projectStore.project.description.length !==
      projectStore.project.specification?.length
);

const name = computed(() => projectStore.project.name || "Project Overview");

const versionLabel = computed(
  () => `Version ${versionToString(projectStore.project.projectVersion)}`
);

const description = computed(
  () =>
    projectStore.project.description ||
    "This project does not have a description."
);

const specification = computed(() => projectStore.project.specification);
</script>
