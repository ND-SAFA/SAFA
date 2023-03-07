<template>
  <private-page>
    <typography
      el="h1"
      y="10"
      align="center"
      variant="large"
      value="Welcome to SAFA!"
    />
    <div class="row">
      <div class="col q-mr-md">
        <panel-card title="Load Existing Project" icon="home-list">
          <typography
            variant="small"
            value="Select an existing project and version to load."
          />
          <project-version-stepper minimal />
        </panel-card>
      </div>
      <div class="col">
        <panel-card title="Create New Project" icon="home-add">
          <typography
            variant="small"
            value="Chose which data source you would like to create a project from."
          />
          <flex-box full-width justify="center" t="2">
            <flex-box column>
              <text-button
                text
                label="Create New Project"
                icon="add"
                color="primary"
                @click="handleOpenStandard"
              />
              <text-button
                text
                label="Bulk Upload Project"
                icon="upload"
                color="primary"
                @click="handleOpenBulk"
              />
              <text-button
                text
                label="Import Jira/GitHub Project"
                icon="integrate"
                color="primary"
                @click="handleOpenImport"
              />
            </flex-box>
          </flex-box>
        </panel-card>
      </div>
    </div>
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
  FlexBox,
  Typography,
  PanelCard,
  TextButton,
  ProjectVersionStepper,
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
