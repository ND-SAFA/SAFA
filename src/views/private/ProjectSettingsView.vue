<template>
  <private-page>
    <template v-slot:page>
      <back-button text="Back To Tree View" to-project />
      <v-container>
        <settings-general-section :project="project" />
        <settings-member-section :project="project" />
      </v-container>
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { projectStore } from "@/hooks";
import {
  PrivatePage,
  SettingsGeneralSection,
  SettingsMemberSection,
  BackButton,
} from "@/components";

/**
 * Displays project settings.
 */
export default Vue.extend({
  name: "ProjectSettingsView",
  components: {
    BackButton,
    PrivatePage,
    SettingsGeneralSection,
    SettingsMemberSection,
  },
  computed: {
    /**
     * @return The current project.
     */
    project() {
      return projectStore.project;
    },
  },
});
</script>
