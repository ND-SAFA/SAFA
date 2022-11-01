<template>
  <private-page>
    <template v-slot:page>
      <typography
        el="h1"
        y="10"
        align="center"
        variant="large"
        value="Welcome to SAFA!"
      />
      <v-row>
        <v-col cols="6">
          <v-card outlined>
            <v-card-title>
              <v-icon large :color="iconColor">
                mdi-folder-plus-outline
              </v-icon>
              <typography
                el="h2"
                l="2"
                variant="subtitle"
                value="Create New Project"
              />
            </v-card-title>
            <v-card-subtitle>
              <v-divider class="mb-2" />
              <typography
                variant="small"
                value="Chose which data source you would like to create a project from."
              />
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
              <v-icon large :color="iconColor"> mdi-view-list </v-icon>
              <typography
                el="h2"
                l="2"
                variant="subtitle"
                value="Load Existing Project"
              />
            </v-card-title>
            <v-card-subtitle>
              <v-divider class="mb-2" />
              <typography
                variant="small"
                value="Select an existing project and version to load."
              />
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
import { CreatorTabTypes } from "@/types";
import { ThemeColors } from "@/util";
import { navigateTo, QueryParams, Routes } from "@/router";
import { PrivatePage, ProjectVersionList, Typography } from "@/components";

/**
 * Displays the home page.
 */
export default Vue.extend({
  name: "HomeView",
  components: {
    PrivatePage,
    ProjectVersionList,
    Typography,
  },
  data() {
    return {
      iconColor: ThemeColors.primary,
    };
  },
  methods: {
    handleOpenStandard() {
      navigateTo(Routes.PROJECT_CREATOR, {
        [QueryParams.TAB]: CreatorTabTypes.standard,
      });
    },
    handleOpenBulk() {
      navigateTo(Routes.PROJECT_CREATOR, {
        [QueryParams.TAB]: CreatorTabTypes.bulk,
      });
    },
    handleOpenGitHub() {
      navigateTo(Routes.PROJECT_CREATOR, {
        [QueryParams.TAB]: CreatorTabTypes.github,
      });
    },
    handleOpenJira() {
      navigateTo(Routes.PROJECT_CREATOR, {
        [QueryParams.TAB]: CreatorTabTypes.jira,
      });
    },
  },
});
</script>
