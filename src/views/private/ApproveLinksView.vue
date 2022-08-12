<template>
  <private-page>
    <template v-slot:page>
      <back-button text="Back To Tree View" />
      <trace-link-table />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { PrivatePage, BackButton, TraceLinkTable } from "@/components";

export default Vue.extend({
  name: "ApproveLinksView",
  components: { TraceLinkTable, BackButton, PrivatePage },
});
</script>
