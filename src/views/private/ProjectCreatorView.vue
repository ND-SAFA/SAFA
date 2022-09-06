<template>
  <private-page>
    <template v-slot:page>
      <project-creator />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { PrivatePage, ProjectCreator } from "@/components";

/**
 * Displays the steps for creating a project.
 */
export default Vue.extend({
  name: "ProjectCreatorView",
  components: {
    ProjectCreator,
    PrivatePage,
  },
});
</script>
