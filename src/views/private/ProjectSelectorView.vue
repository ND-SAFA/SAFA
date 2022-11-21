<template>
  <private-page>
    <template v-slot:page>
      <project-version-stepper />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { PrivatePage, ProjectVersionStepper } from "@/components";

/**
 * Displays the steps for creating a project.
 */
export default Vue.extend({
  name: "ProjectCreatorView",
  components: {
    ProjectVersionStepper,
    PrivatePage,
  },
});
</script>
