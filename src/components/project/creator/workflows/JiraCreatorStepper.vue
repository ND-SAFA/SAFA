<template>
  <generic-stepper
    v-model="currentStep"
    :steps="steps"
    submitText="Create Project"
    @submit="handleSaveProject()"
  >
    <template v-slot:items>
      <v-stepper-content step="1">
        <jira-authentication :token="token" />
      </v-stepper-content>

      <v-stepper-content step="2">
        <jira-site-selector
          :loading="sitesLoading"
          :sites="sites"
          @select="handleSiteSelect($event)"
        />
      </v-stepper-content>

      <v-stepper-content step="3">
        <jira-project-selector
          :loading="projectsLoading"
          :projects="projects"
          @select="handleProjectSelect($event)"
        />
      </v-stepper-content>
    </template>
  </generic-stepper>
</template>

<script lang="ts">
import Vue from "vue";
import { JiraCloudSite, JiraProject, StepState } from "@/types";
import { getParam, QueryParams } from "@/router";
import { logModule } from "@/store";
import { getJiraToken, getJiraProjects, getJiraCloudSites } from "@/api";
import { GenericStepper } from "@/components/common";
import {
  JiraAuthentication,
  JiraSiteSelector,
  JiraProjectSelector,
} from "@/components/project/creator/steps";

/**
 * Allows for creating a project from Jira.
 */
export default Vue.extend({
  components: {
    JiraProjectSelector,
    JiraSiteSelector,
    JiraAuthentication,
    GenericStepper,
  },
  data() {
    return {
      accessCode: getParam(QueryParams.JIRA_TOKEN),
      token: "",

      sites: [] as JiraCloudSite[],
      sitesLoading: false,
      selectedSite: undefined as JiraCloudSite | undefined,

      projects: [] as JiraProject[],
      projectsLoading: false,
      selectedProject: undefined as JiraProject | undefined,

      steps: [
        ["Connect to Jira", false],
        ["Select Domain", false],
        ["Select Project", false],
      ] as StepState[],
      currentStep: 1,
    };
  },
  mounted() {
    if (!this.accessCode) return;

    this.loadToken().then(async () => {
      this.setStepIsValid(0, true);
      this.currentStep = 2;

      await this.loadSites();
    });
  },
  methods: {
    setStepIsValid(stepIndex: number, isValid: boolean): void {
      Vue.set(this.steps, stepIndex, [this.steps[stepIndex][0], isValid]);
    },

    clearData(): void {
      this.token = "";
      this.sites = [];
      this.projects = [];
    },
    async loadToken() {
      if (!this.accessCode) return;

      this.token = await getJiraToken(String(this.accessCode));
    },
    async loadSites() {
      if (!this.token) return;

      this.sitesLoading = true;
      this.sites = await getJiraCloudSites(this.token);
      this.sitesLoading = false;
    },
    async loadProjects() {
      if (!this.selectedSite || !this.token) return;

      this.projectsLoading = true;
      this.projects = await getJiraProjects(this.token, this.selectedSite.id);
      this.projectsLoading = false;
    },

    handleSiteSelect(site: JiraCloudSite) {
      if (this.selectedSite?.id !== site.id) {
        this.selectedSite = site;
        this.setStepIsValid(1, true);
        this.currentStep = 3;
        this.loadProjects();
      } else {
        this.selectedSite = undefined;
        this.setStepIsValid(1, false);
      }
    },
    handleProjectSelect(project: JiraProject) {
      if (this.selectedProject?.id !== project.id) {
        this.selectedProject = project;
        this.setStepIsValid(2, true);
      } else {
        this.selectedProject = undefined;
        this.setStepIsValid(2, false);
      }
    },
    handleSaveProject(): void {
      logModule.onInfo("Jira projects can not yet be created");
      // TODO: when endpoint exists:
      // appModule.onLoadStart();
      // saveOrUpdateProject(this.project)
      //   .then(async (res) => {
      //     this.clearData();
      //     await navigateTo(Routes.ARTIFACT);
      //     await setCreatedProject(res);
      //   })
      //   .finally(() => {
      //     appModule.onLoadEnd();
      //   });
    },
  },
});
</script>
