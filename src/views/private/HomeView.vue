<template>
  <private-page>
    <template v-slot:page>
      <h1 class="text-h3 text-center mt-10">Welcome to SAFA!</h1>
      <p class="text-body-1 text-center mb-10">
        You can either open an existing project, or create a new one.
      </p>
      <v-row>
        <v-col cols="6">
          <v-card elevation="1">
            <div class="mx-auto width-fit pt-6">
              <v-icon style="font-size: 80px" :color="iconColor">
                mdi-folder-plus-outline
              </v-icon>
            </div>
            <v-card-title>
              <h2 class="text-h5">Create New Project</h2>
            </v-card-title>
            <v-card-text>
              <v-divider class="mb-2" />
              <div class="mx-auto width-min">
                <v-btn text @click="handleOpenStandard">
                  <v-icon>mdi-plus</v-icon>
                  Create New Project
                </v-btn>
                <v-btn text @click="handleOpenBulk">
                  <v-icon>mdi-folder-arrow-up-outline</v-icon>
                  Bulk Upload Project
                </v-btn>
                <v-btn text @click="handleOpenGitHub">
                  <v-icon>mdi-transit-connection-variant</v-icon>
                  Create GitHub Project
                </v-btn>
                <v-btn text @click="handleOpenJira">
                  <v-icon>mdi-transit-connection-variant</v-icon>
                  Create Jira Project
                </v-btn>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="6">
          <v-card elevation="1">
            <div class="mx-auto width-fit pt-6">
              <v-icon style="font-size: 80px" :color="iconColor">
                mdi-view-list
              </v-icon>
            </div>
            <v-card-title>
              <h2 class="text-h5">Load Existing Project</h2>
            </v-card-title>
            <v-card-text>
              <v-divider class="mb-2" />
              <project-version-list />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { CreatorTypes } from "@/types";
import { PrivatePage, ProjectVersionList } from "@/components";
import { ThemeColors } from "@/util";
import { navigateTo, QueryParams, Routes } from "@/router";

/**
 * Displays the home page.
 */
export default Vue.extend({
  name: "HomeView",
  components: {
    PrivatePage,
    ProjectVersionList,
  },
  data() {
    return {
      iconColor: ThemeColors.primary,
    };
  },
  methods: {
    handleOpenStandard() {
      navigateTo(Routes.PROJECT_CREATOR, {
        [QueryParams.TAB]: CreatorTypes.standard,
      });
    },
    handleOpenBulk() {
      navigateTo(Routes.PROJECT_CREATOR, {
        [QueryParams.TAB]: CreatorTypes.bulk,
      });
    },
    handleOpenGitHub() {
      navigateTo(Routes.PROJECT_CREATOR, {
        [QueryParams.TAB]: CreatorTypes.github,
      });
    },
    handleOpenJira() {
      navigateTo(Routes.PROJECT_CREATOR, {
        [QueryParams.TAB]: CreatorTypes.jira,
      });
    },
  },
});
</script>
