<template>
  <panel-card data-cy="tab-bulk-upload">
    <project-files-uploader
      data-cy-name="input-project-name-bulk"
      data-cy-description="input-project-description-bulk"
    />
  </panel-card>
</template>

<script lang="ts">
/**
 * Allows for creating a project with a bulk upload.
 */
export default {
  name: "ProjectBulkUpload",
};
</script>

<script setup lang="ts">
import { ProjectFilesUploader } from "@/components/project/save";
import { PanelCard } from "@/components/common";
</script>
