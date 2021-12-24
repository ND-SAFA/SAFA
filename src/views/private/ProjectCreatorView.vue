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
 * Displays the steps for defining a project.
 */
export default Vue.extend({
  components: {
    ProjectCreator,
    PrivatePage,
  },
});
</script>
