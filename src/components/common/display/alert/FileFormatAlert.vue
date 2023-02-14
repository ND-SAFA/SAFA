<template>
  <v-alert outlined dense border="left" color="primary">
    <typography
      color="primary"
      value="The format of files can be found here:"
    />
    <v-btn text link color="primary" @click="handleOpenWiki">SAFA WIKI</v-btn>
  </v-alert>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Typography from "../Typography.vue";

/**
 * An alert that details the required format of upload files.
 */
export default defineComponent({
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
