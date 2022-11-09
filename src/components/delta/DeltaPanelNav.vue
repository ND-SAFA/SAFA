<template>
  <div class="mt-4">
    <v-btn
      v-if="!isSelectorVisible"
      block
      large
      color="primary"
      @click="handleChange"
    >
      <v-icon class="pr-2">mdi-source-branch</v-icon>
      Compare Versions
    </v-btn>
    <v-btn v-else block large outlined @click="handleChange">
      <v-icon class="pr-2">mdi-close</v-icon>
      Hide Delta View
    </v-btn>

    <v-select
      v-if="isSelectorVisible"
      filled
      v-model="version"
      :items="versions"
      :loading="isLoading"
      item-value="versionId"
      label="Delta Version"
      class="mt-4"
    >
      <template v-slot:selection>
        {{ getVersionName(version) }}
      </template>
      <template v-slot:item="{ item }">
        {{ getVersionName(item) }}
      </template>
    </v-select>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { VersionModel } from "@/types";
import { versionToString } from "@/util";
import { deltaStore, projectStore } from "@/hooks";
import {
  getProjectVersions,
  handleReloadProject,
  handleSetProjectDelta,
} from "@/api";

/**
 * Displays the delta panel navigation.
 */
export default Vue.extend({
  name: "DeltaPanelNav",
  components: {},
  data() {
    return {
      isLoading: false,
      isSelectorVisible: deltaStore.inDeltaView,
      versions: [] as VersionModel[],
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
     * @return Whether delta view is enabled.
     */
    inDeltaView(): boolean {
      return deltaStore.inDeltaView;
    },
    /**
     * Tracks the delta version and loads new versions.
     */
    version: {
      get(): VersionModel | undefined {
        return deltaStore.afterVersion;
      },
      set(newVersionId: string): void {
        const newVersion = this.versions.find(
          ({ versionId }) => versionId === newVersionId
        );

        if (!newVersion || !this.project.projectVersion) return;

        this.isLoading = true;

        handleSetProjectDelta(this.project.projectVersion, newVersion, () => {
          this.isLoading = false;
        });
      },
    },
  },
  methods: {
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
    async loadVersions(): Promise<void> {
      const { projectId } = this.project;
      this.versions = projectId ? await getProjectVersions(projectId) : [];
    },
    /**
     * Changes whether delta view is enabled.
     */
    handleChange(): void {
      if (this.isSelectorVisible) {
        deltaStore.setIsDeltaViewEnabled(false);
        handleReloadProject();
        this.isSelectorVisible = false;
      } else {
        this.isSelectorVisible = true;
      }
    },
    /**
     * Enables delta view.
     */
    handleSubmit(): void {
      deltaStore.setIsDeltaViewEnabled(true);
    },
  },
});
</script>
