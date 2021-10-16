<template>
  <v-container>
    <v-row justify="center" class="mt-5">
      <v-container>
        <v-row justify="center">
          <h3 style="text-align: center" class="mt-3 mb-3">
            {{ projectSelectorTitle }}
          </h3>
        </v-row>
        <v-row justify="center">
          <ProjectSelector
            :isOpen="isOpen"
            @onProjectSelected="$emit('onProjectSelected', $event)"
            @onProjectUnselected="$emit('onProjectUnselected', $event)"
          />
        </v-row>
      </v-container>
    </v-row>
    <v-row justify="center" class="mt-5">
      <v-container>
        <v-row justify="center">
          <h3 style="text-align: center" class="mt-3 mb-3">
            {{ versionSelectorTitle }}
          </h3>
        </v-row>
        <v-row justify="center">
          <VersionSelector
            v-if="selectedProject !== undefined"
            :isOpen="isOpen"
            :project="selectedProject"
            @onVersionSelected="$emit('onVersionSelected', $event)"
            @onVersionUnselected="$emit('onVersionUnselected', $event)"
          />
          <p v-else>No project selected</p>
        </v-row>
      </v-container>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { ProjectIdentifier, ProjectVersion } from "@/types/domain/project";
import ProjectSelector from "@/components/common/modals/ProjectSelector.vue";
import VersionSelector from "@/components/common/modals/VersionSelector.vue";
import Vue, { PropType } from "vue";
export default Vue.extend({
  components: {
    ProjectSelector,
    VersionSelector,
  },
  props: {
    projectSelectorTitle: {
      type: String,
      required: true,
    },
    versionSelectorTitle: {
      type: String,
      required: true,
    },
    isOpen: {
      type: Boolean,
      required: true,
    },
    selectedProject: {
      type: Object as PropType<ProjectIdentifier>,
    },
    selectedVersion: {
      type: Object as PropType<ProjectVersion>,
    },
  },
});
</script>
