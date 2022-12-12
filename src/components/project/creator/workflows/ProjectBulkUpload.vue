<template>
  <panel-card data-cy="tab-bulk-upload">
    <project-files-uploader
      data-cy-name="input-project-name-bulk"
      data-cy-description="input-project-description-bulk"
    />
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { ProjectFilesUploader } from "@/components/project/base";
import { PanelCard } from "@/components/common";

/**
 * Allows for creating a project with a bulk upload.
 */
export default Vue.extend({
  name: "ProjectBulkUpload",
  components: {
    PanelCard,
    ProjectFilesUploader,
  },
});
</script>
