<template>
  <alert-card>
    <flex-box align="center">
      <typography
        color="primary"
        value="The format of files can be found here:"
      />
      <q-btn flat color="primary" @click="handleOpenWiki">
        <typography value="SAFA WIKI" />
      </q-btn>
    </flex-box>
  </alert-card>
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
import { Typography, FlexBox } from "../content";
import AlertCard from "./AlertCard.vue";

/**
 * Opens the SAFA WIKI docs.
 */
function handleOpenWiki() {
  window.open(
    "https://www.notion.so/nd-safa/Project-Creation-5ececa9fd233437ebb37ddf893d394df#6532e1d3f983453898a8bf6ffda007f4"
  );
}
</script>
