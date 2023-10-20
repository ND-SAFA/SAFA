<template>
  <private-page small-window>
    <typography
      el="h1"
      b="5"
      align="center"
      variant="large"
      value="Welcome to SAFA"
    />
    <flex-box :column="smallWindow">
      <flex-item :parts="smallWindow ? '12' : '7'">
        <div :class="smallWindow ? '' : 'q-mr-md'">
          <panel-card
            v-if="projectStore.allProjects.length > 0"
            title="Load Existing Project"
            icon="nav-open"
          >
            <typography
              variant="small"
              value="Select an existing project and version to load."
            />
            <project-version-stepper minimal />
          </panel-card>
        </div>
      </flex-item>
      <flex-item :parts="smallWindow ? '12' : '5'">
        <panel-card title="Create New Project" icon="project-add">
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
        <external-links />
      </flex-item>
    </flex-box>
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
import { CreatorTab } from "@/types";
import { projectStore, useScreen } from "@/hooks";
import { navigateTo, QueryParams, Routes } from "@/router";
import {
  ExternalLinks,
  PrivatePage,
  FlexBox,
  Typography,
  PanelCard,
  TextButton,
  ProjectVersionStepper,
  FlexItem,
} from "@/components";

const { smallWindow } = useScreen();

function handleOpenStandard() {
  navigateTo(Routes.PROJECT_CREATOR, {
    [QueryParams.TAB]: "standard" as CreatorTab,
  });
}

function handleOpenBulk() {
  navigateTo(Routes.PROJECT_CREATOR, {
    [QueryParams.TAB]: "bulk" as CreatorTab,
  });
}

function handleOpenImport() {
  navigateTo(Routes.PROJECT_CREATOR, {
    [QueryParams.TAB]: "import" as CreatorTab,
  });
}
</script>
