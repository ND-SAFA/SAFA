<template>
  <v-container>
    <typography t="4" el="h1" variant="title" value="Project Uploads" />
    <v-divider />
    <typography
      el="p"
      y="2"
      value="Select an upload below to see more details on its status."
    />
    <job-table />
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { Typography } from "@/components/common";
import JobTable from "./JobTable.vue";

/**
 * Displays all upload jobs.
 */
export default Vue.extend({
  name: "JobDisplay",
  components: { Typography, JobTable },
  props: {},
  data() {
    return {};
  },
  computed: {},
  methods: {},
});
</script>

<style scoped lang="scss"></style>
