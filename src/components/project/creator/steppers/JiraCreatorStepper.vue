<template>
  <generic-stepper
    v-model="currentStep"
    :steps="steps"
    submitText="Create Project"
    @submit="handleSaveProject()"
  >
    <template v-slot:items>
      <v-stepper-content step="1">
        <v-container class="d-flex justify-center">
          <v-btn
            large
            class="my-10"
            color="primary"
            :disabled="!!token"
            @click="handleJiraAuthentication"
          >
            <span v-if="!token">Connect to Jira</span>
            <span v-else>Connected to Jira</span>
          </v-btn>
        </v-container>
      </v-stepper-content>

      <v-stepper-content step="2">
        <h1 class="text-h5">Jira Domains</h1>
        <v-divider />
        <v-list>
          <v-list-item-group>
            <template v-for="site in sites">
              <v-list-item :key="site.id" @click="handleSiteSelect(site)">
                <v-list-item-content>
                  <v-list-item-title v-text="site.name" />

                  <v-list-item-subtitle v-text="site.url" />
                </v-list-item-content>
              </v-list-item>
            </template>
          </v-list-item-group>
        </v-list>
      </v-stepper-content>

      <v-stepper-content step="3">
        <h1 class="text-h5">Jira Projects</h1>
        <v-divider />
        <v-list>
          <v-list-item-group>
            <template v-for="project in projects">
              <v-list-item
                :key="project.id"
                @click="handleProjectSelect(project)"
              >
                <v-list-item-content>
                  <v-list-item-title v-text="project.name" />
                </v-list-item-content>
              </v-list-item>
            </template>
          </v-list-item-group>
        </v-list>
      </v-stepper-content>
    </template>
  </generic-stepper>
</template>

<script lang="ts">
import Vue from "vue";
import { JiraCloudSite, JiraProject, StepState } from "@/types";
import { getParam, QueryParams } from "@/router";
import {
  authorizeJira,
  getJiraToken,
  getJiraProjects,
  getJiraCloudSites,
} from "@/api";
import { GenericStepper } from "@/components/common";

/**
 * Allows for creating a project from JIRA.
 */
export default Vue.extend({
  components: { GenericStepper },
  data() {
    return {
      accessCode: getParam(QueryParams.JIRA_TOKEN),
      token: "",

      sites: [
        {
          id: "1",
          name: "Site 1",
          url: "example1.atlassian.net",
        },
        {
          id: "2",
          name: "Site 2",
          url: "example2.atlassian.net",
        },
        {
          id: "3",
          name: "Site 3",
          url: "example3.atlassian.net",
        },
      ] as JiraCloudSite[], // TODO: remove test
      selectedSite: undefined as JiraCloudSite | undefined,

      projects: [
        {
          id: "1",
          name: "Project 1",
        },
        {
          id: "2",
          name: "Project 2",
        },
      ] as JiraProject[], // TODO: remove test
      selectedProject: undefined as JiraProject | undefined,

      steps: [
        ["Connect to Jira", false],
        ["Select Domain", false],
        ["Select Project", false],
      ] as StepState[],
      currentStep: 2, // TODO: remove test
    };
  },
  async mounted() {
    if (!this.accessCode) return;

    this.setStepIsValid(0, true);
    this.currentStep = 2;

    await this.loadToken();
    await this.loadSites();
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

      this.sites = await getJiraCloudSites(this.token);
    },
    async loadProjects() {
      if (!this.selectedSite || !this.token) return;

      this.projects = await getJiraProjects(this.token, this.selectedSite.id);
    },

    handleJiraAuthentication(): void {
      authorizeJira();
    },
    handleSiteSelect(site: JiraCloudSite) {
      if (this.selectedSite?.id !== site.id) {
        this.selectedSite = site;
        this.setStepIsValid(1, true);
        this.currentStep = 3;
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
