<template>
  <v-card outlined elevation="1" data-cy="tab-bulk-upload">
    <project-identifier-input
      v-bind:name.sync="name"
      v-bind:description.sync="description"
      data-cy-name="input-project-name-bulk"
      data-cy-description="input-project-description-bulk"
    />
    <project-files-input
      v-bind:name.sync="name"
      v-bind:description.sync="description"
    />
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import {
  ProjectFilesInput,
  ProjectIdentifierInput,
} from "@/components/project/shared";

/**
 * Allows for creating a project with a bulk upload.
 */
export default Vue.extend({
  name: "ProjectBulkUpload",
  components: {
    ProjectFilesInput,
    ProjectIdentifierInput,
  },
  data() {
    return {
      name: "",
      description: "",
    };
  },
});
</script>
