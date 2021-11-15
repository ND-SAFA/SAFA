<template>
  <v-container>
    <ProjectCreator />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { ProjectCreator } from "@/components/project";

export default Vue.extend({
  components: {
    ProjectCreator,
  },
});
</script>
