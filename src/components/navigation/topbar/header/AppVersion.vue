<template>
  <flex-box align="center">
    <typography
      el="h1"
      variant="subtitle"
      color="accent"
      style="white-space: nowrap"
      :value="projectName"
      x="4"
    />
    <v-select
      v-if="isProjectDefined"
      outlined
      hide-details
      dark
      dense
      label="Version"
      :value="version"
      :items="versions"
      item-value="versionId"
      style="width: 100px"
      @input="handleLoadVersion"
    >
      <template v-slot:selection>
        {{ getVersionName(version) }}
      </template>
      <template v-slot:item="{ item }">
        {{ getVersionName(item) }}
      </template>
      <template v-slot:append-item>
        <v-btn text color="primary" @click="openCreateVersion = true">
          <v-icon>mdi-plus</v-icon>
          Add Version
        </v-btn>
      </template>
    </v-select>

    <version-creator
      :is-open="openCreateVersion"
      :project="project"
      @close="openCreateVersion = false"
      @create="handleVersionCreated"
    />
  </flex-box>
</template>

<script lang="ts">
import Vue from "vue";
import { VersionModel } from "@/types";
import { versionToString } from "@/util";
import { projectStore } from "@/hooks";
import { getProjectVersions, handleLoadVersion } from "@/api";
import { Typography, FlexBox } from "@/components/common";
import { VersionCreator } from "@/components/project/selector";

/**
 * Displays the current project version.
 */
export default Vue.extend({
  name: "AppVersion",
  components: { FlexBox, Typography, VersionCreator },
  data() {
    return {
      versions: [] as VersionModel[],
      openCreateVersion: false,
    };
  },
  mounted() {
    this.loadVersions();
  },
  computed: {
    /**
     * @return The current project.
     */
    project() {
      return projectStore.project;
    },
    /**
     * @return The current version.
     */
    version() {
      return projectStore.project.projectVersion;
    },
    /**
     * @return Whether a project is currently loaded.
     */
    isProjectDefined(): boolean {
      return projectStore.isProjectDefined;
    },
    /**
     * @return The name of this project.
     */
    projectName(): string {
      return this.isProjectDefined ? this.project.name : "No Project Selected";
    },
  },
  methods: {
    /**
     * Loads the versions of the current project.
     */
    async loadVersions(): Promise<void> {
      const { projectId } = this.project;
      this.versions = projectId ? await getProjectVersions(projectId) : [];
    },
    /**
     * Returns a version's name.
     * @param version - The version to name.
     * @return The version's name.
     */
    getVersionName(version: VersionModel): string {
      return versionToString(version);
    },
    /**
     * Loads the versions of the current project.
     */
    async handleLoadVersion(versionId: string): Promise<void> {
      await handleLoadVersion(versionId);
    },
    /**
     * Adds the new version the version list and loads that version.
     * @param version - The new version.
     */
    async handleVersionCreated(version: VersionModel): Promise<void> {
      this.versions = [version, ...this.versions];
      this.openCreateVersion = false;
      await handleLoadVersion(version.versionId);
    },
  },
  watch: {
    project() {
      this.loadVersions();
    },
  },
});
</script>
