<template>
  <v-card outlined elevation="1" data-cy="tab-bulk-upload">
    <project-files-uploader
      data-cy-name="input-project-name-bulk"
      data-cy-description="input-project-description-bulk"
    />
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import { ProjectFilesUploader } from "@/components/project/shared";

/**
 * Allows for creating a project with a bulk upload.
 */
export default Vue.extend({
  name: "ProjectBulkUpload",
  components: {
    ProjectFilesUploader,
  },
});
</script>
