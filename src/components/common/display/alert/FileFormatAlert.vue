<template>
  <alert>
    <flex-box align="center">
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
    </flex-box>
  </alert>
</template>

<script lang="ts">
/**
 * An alert that details the required format of upload files.
 */
export default {
  name: "FileFormatAlert",
};
</script>

<script setup lang="ts">
import TextButton from "@/components/common/button/TextButton.vue";
import FlexBox from "@/components/common/layout/FlexBox.vue";
import Typography from "../Typography.vue";
import Alert from "./Alert.vue";

/**
 * Opens the SAFA WIKI docs.
 */
function handleOpenWiki() {
  window.open(
    "https://www.notion.so/nd-safa/Project-Creation-5ececa9fd233437ebb37ddf893d394df#6532e1d3f983453898a8bf6ffda007f4"
  );
}
</script>
