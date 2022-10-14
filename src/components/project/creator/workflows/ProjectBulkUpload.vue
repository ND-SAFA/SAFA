<template>
  <v-card outlined elevation="1" data-cy="tab-bulk-upload">
    <project-identifier-input
      v-bind:name.sync="name"
      v-bind:description.sync="description"
      data-cy-name="input-project-name-bulk"
      data-cy-description="input-project-description-bulk"
    />
    <project-files-uploader
      v-bind:name.sync="name"
      v-bind:description.sync="description"
      data-cy-name="input-project-name-bulk"
      data-cy-description="input-project-description-bulk"
    />
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import {
  ProjectFilesUploader,
  ProjectIdentifierInput,
} from "@/components/project/shared";

/**
 * Allows for creating a project with a bulk upload.
 */
export default Vue.extend({
  name: "ProjectBulkUpload",
  components: {
    ProjectFilesUploader,
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
