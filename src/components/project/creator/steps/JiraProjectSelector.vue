<template>
  <generic-stepper-list-step
    empty-message="There are no projects."
    :item-count="projects.length"
    :loading="loading"
    title="Jira Projects"
  >
    <template slot="items">
      <template v-for="project in projects">
        <v-list-item :key="project.id" @click="handleProjectSelect(project)">
          <v-list-item-icon>
            <v-avatar>
              <img :src="project.avatarUrls['48x48']" :alt="project.name" />
            </v-avatar>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="project.name" />

            <v-list-item-subtitle v-text="getProjectSubtitle(project)" />
          </v-list-item-content>
        </v-list-item>
      </template>
    </template>
  </generic-stepper-list-step>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { JiraProjectModel } from "@/types";
import { GenericStepperListStep } from "@/components";

/**
 * Allows for selecting a jira project.
 *
 * @emits `select` (JiraProject) - On project selection.
 */
export default Vue.extend({
  name: "JiraProjectSelector",
  components: {
    GenericStepperListStep,
  },
  props: {
    projects: {
      type: Array as PropType<JiraProjectModel[]>,
      required: true,
    },
    loading: {
      type: Boolean,
      required: false,
    },
  },
  methods: {
    /**
     * Handles a click to select a project.
     * @param project - The project to select.
     */
    handleProjectSelect(project: JiraProjectModel) {
      this.$emit("select", project);
    },
    /**
     * Returns a project's subtitle.
     * @param project - The project to extract from.
     * @return The subtitle.
     */
    getProjectSubtitle(project: JiraProjectModel): string {
      const {
        key,
        insight: { totalIssueCount },
      } = project;
      const subtitle = `${key} | ${totalIssueCount} Issue`;

      return totalIssueCount === 1 ? subtitle : `${subtitle}s`;
    },
  },
});
</script>
