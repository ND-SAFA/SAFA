<template>
  <alert>
    <typography
      color="primary"
      value="The format of files can be found here:"
    />
    <text-button
      text
      label="SAFA WIKI"
      color="primary"
      @click="handleOpenWiki"
    />
  </alert>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import TextButton from "@/components/common/button/TextButton.vue";
import Typography from "../Typography.vue";
import Alert from "./Alert.vue";

/**
 * An alert that details the required format of upload files.
 */
export default defineComponent({
  name: "FileFormatAlert",
  components: { TextButton, Alert, Typography },
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
