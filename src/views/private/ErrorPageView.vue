<template>
  <private-page>
    <v-row justify="center">
      <v-col align-self="center">
        <safa-icon />
        <typography
          value="Sorry, an error has occurred. Please refresh your browser and try
            again."
        />
      </v-col>
    </v-row>
  </private-page>
</template>

<script lang="ts">
/**
 * The default page displayed if an unknown error is encountered.
 */
export default {
  name: "ErrorPageView",
};
</script>

<script setup lang="ts">
import { PrivatePage, SafaIcon, Typography } from "@/components";
</script>
