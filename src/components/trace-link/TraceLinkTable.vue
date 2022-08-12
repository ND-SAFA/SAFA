<template>
  <v-container>
    <v-data-table
      show-group-by
      show-expand
      fixed-header
      :headers="headers"
      :items="links"
      :expanded="expanded"
      sort-by="targetName"
      :items-per-page="50"
    >
      <template v-slot:top>
        <v-text-field
          dense
          outlined
          clearable
          label="Search Trace Links"
          style="max-width: 600px"
          v-model="searchText"
          append-icon="mdi-magnify"
        />
      </template>

      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length"></td>
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { ApprovalType, TraceLinkModel, VersionModel } from "@/types";
import { projectModule } from "@/store";
import { getGeneratedLinks } from "@/api";

/**
 * Displays a table of trace links.
 */
export default Vue.extend({
  name: "TraceLinkTable",

  data() {
    return {
      searchText: "",
      headers: [
        {
          text: "Source Name",
          value: "sourceName",
          filterable: true,
          divider: true,
        },
        {
          text: "Target Name",
          value: "targetName",
          filterable: true,
          divider: true,
        },
        {
          value: "data-table-expand",
          groupable: false,
        },
      ],
      links: [] as TraceLinkModel[],
      expanded: [] as TraceLinkModel[],
      approved: [] as string[],
      declined: [] as string[],
    };
  },
  mounted() {
    this.loadGeneratedLinks();
  },
  watch: {
    /**
     * Loads generated links when the version changes.
     */
    projectVersion(newVersion?: VersionModel) {
      if (!newVersion) return;

      this.loadGeneratedLinks();
    },
  },
  computed: {
    /**
     * @return The current project version.
     */
    projectVersion() {
      return projectModule.getProject.projectVersion;
    },
  },
  methods: {
    /**
     * Loads the generated links for the current project.
     */
    async loadGeneratedLinks() {
      const versionId = projectModule.versionIdWithLog;
      this.links = await getGeneratedLinks(versionId);
      this.approved = [];
      this.declined = [];

      this.links.forEach((link) => {
        if (link.approvalStatus === ApprovalType.APPROVED) {
          this.approved.push(link.traceLinkId);
        } else if (link.approvalStatus === ApprovalType.DECLINED) {
          this.declined.push(link.traceLinkId);
        }
      });
    },
    /**
     * Approves the given link and updates the stored links.
     *
     * @param link - The link to approve.
     */
    handleApprove(link: TraceLinkModel) {
      this.declined = this.declined.filter(
        (declinedId) => declinedId != link.traceLinkId
      );
      this.approved.push(link.traceLinkId);
    },
    /**
     * Declines the given link and updates the stored links.
     *
     * @param link - The link to decline.
     */
    handleDecline(link: TraceLinkModel) {
      this.approved = this.approved.filter(
        (declinedId) => declinedId != link.traceLinkId
      );
      this.declined.push(link.traceLinkId);
    },
  },
});
</script>

<style scoped></style>
