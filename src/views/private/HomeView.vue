<template>
  <private-page>
    <typography
      el="h1"
      y="10"
      align="center"
      variant="large"
      value="Welcome to SAFA!"
    />
    <v-row>
      <v-col cols="6">
        <panel-card>
          <v-card-title>
            <v-icon large color="primary"> mdi-view-list </v-icon>
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
            <mini-project-version-stepper />
          </v-card-text>
        </panel-card>
      </v-col>
      <v-col cols="6">
        <panel-card>
          <v-card-title>
            <v-icon large color="primary"> mdi-folder-plus-outline </v-icon>
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
              <v-btn text @click="handleOpenImport">
                <v-icon>mdi-transit-connection-variant</v-icon>
                Import Jira/GitHub Project
              </v-btn>
            </div>
          </v-card-text>
        </panel-card>
      </v-col>
    </v-row>
  </private-page>
</template>

<script lang="ts">
/**
 * Displays the home page.
 */
export default {
  name: "HomeView",
};
</script>

<script setup lang="ts">
import { CreatorTabTypes } from "@/types";
import { navigateTo, QueryParams, Routes } from "@/router";
import {
  PrivatePage,
  MiniProjectVersionStepper,
  Typography,
  PanelCard,
} from "@/components";

function handleOpenStandard() {
  navigateTo(Routes.PROJECT_CREATOR, {
    [QueryParams.TAB]: CreatorTabTypes.standard,
  });
}

function handleOpenBulk() {
  navigateTo(Routes.PROJECT_CREATOR, {
    [QueryParams.TAB]: CreatorTabTypes.bulk,
  });
}

function handleOpenImport() {
  navigateTo(Routes.PROJECT_CREATOR, {
    [QueryParams.TAB]: CreatorTabTypes.import,
  });
}
</script>
