<template>
  <private-page>
    <template v-slot:page>
      <typography t="4" el="h1" variant="title" value="Create A Project" />
      <v-divider />
      <typography
        el="p"
        y="2"
        value="Create a project using one of the following methods."
      />
      <project-creator />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { PrivatePage, ProjectCreator, Typography } from "@/components";

/**
 * Displays the steps for creating a project.
 */
export default Vue.extend({
  name: "ProjectCreatorView",
  components: {
    ProjectCreator,
    PrivatePage,
    Typography,
  },
});
</script>
