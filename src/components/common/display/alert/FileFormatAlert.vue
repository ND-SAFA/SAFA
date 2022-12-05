<template>
  <v-alert dense border="left" color="primary">
    <typography color="white" value="The format of files can be found here:" />
    <v-btn text link color="white" @click="handleOpenWiki">SAFA WIKI</v-btn>
  </v-alert>
</template>

<script lang="ts">
import Vue from "vue";
import Typography from "../Typography.vue";

/**
 * An alert that details the required format of upload files.
 */
export default Vue.extend({
  name: "FileFormatAlert",
  components: { Typography },
  methods: {
    /**
     * Opens the SAFA WIKI docs.
     */
    handleOpenWiki() {
      window.open(
        "https://www.notion.so/nd-safa/Project-Creation-5ececa9fd233437ebb37ddf893d394df#6532e1d3f983453898a8bf6ffda007f4"
      );
    },
  },
});
</script>
