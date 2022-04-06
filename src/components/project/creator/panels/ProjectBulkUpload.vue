<template>
  <v-card outlined elevation="1">
    <project-identifier-input
      v-bind:name.sync="name"
      v-bind:description.sync="description"
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
