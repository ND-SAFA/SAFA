<template>
  <private-page>
    <template v-slot:page>
      <h1 class="text-h3 text-center my-10">Welcome to SAFA!</h1>
      <v-row>
        <v-col cols="6">
          <v-card outlined>
            <v-card-title>
              <v-icon style="font-size: 40px" :color="iconColor">
                mdi-folder-plus-outline
              </v-icon>
              <h2 class="text-h5 ml-1">Create New Project</h2>
            </v-card-title>
            <v-card-subtitle>
              <v-divider class="mb-2" />
              <p class="text-subtitle-2">
                Chose which data source you would like to create a project from.
              </p>
            </v-card-subtitle>
            <v-card-text>
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
                  Import GitHub Project
                </v-btn>
                <v-btn text @click="handleOpenJira">
                  <v-icon>mdi-transit-connection-variant</v-icon>
                  Import Jira Project
                </v-btn>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="6">
          <v-card outlined>
            <v-card-title>
              <v-icon style="font-size: 40px" :color="iconColor">
                mdi-view-list
              </v-icon>
              <h2 class="text-h5 ml-1">Load Existing Project</h2>
            </v-card-title>
            <v-card-subtitle>
              <v-divider class="mb-2" />
              <p class="text-subtitle-2">
                Select an existing project and version to load.
              </p>
            </v-card-subtitle>
            <v-card-text>
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
