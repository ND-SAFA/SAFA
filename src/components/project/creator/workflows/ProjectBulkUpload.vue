<template>
  <panel-card data-cy="tab-bulk-upload">
    <project-files-uploader
      data-cy-name="input-project-name-bulk"
      data-cy-description="input-project-description-bulk"
    />
  </panel-card>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { ProjectFilesUploader } from "@/components/project/base";
import { PanelCard } from "@/components/common";

/**
 * Allows for creating a project with a bulk upload.
 */
export default defineComponent({
  name: "ProjectBulkUpload",
  components: {
    PanelCard,
    ProjectFilesUploader,
  },
});
</script>
