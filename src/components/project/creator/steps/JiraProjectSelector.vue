<template>
  <v-container>
    <h1 class="text-h5">Jira Projects</h1>
    <v-divider />
    <v-progress-circular
      v-if="loading"
      indeterminate
      size="48"
      class="mx-auto my-2 d-block"
    />
    <p v-else-if="projects.length === 0" class="text-caption">
      There are no projects.
    </p>
    <v-list>
      <v-list-item-group>
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
      </v-list-item-group>
    </v-list>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { JiraProject } from "@/types";

/**
 * Allows for selecting a jira project.
 *
 * @emits `select` (JiraProject) - On project selection.
 */
export default Vue.extend({
  name: "JiraProjectSelector",
  props: {
    projects: {
      type: Array as PropType<JiraProject[]>,
      required: true,
    },
    loading: {
      type: Boolean,
      required: false,
    },
  },
  methods: {
    handleProjectSelect(project: JiraProject) {
      this.$emit("select", project);
    },
    getProjectSubtitle(project: JiraProject): string {
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
