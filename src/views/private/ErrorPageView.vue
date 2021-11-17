<template>
  <private-page>
    <template v-slot:page>
      <v-row justify="center">
        <v-col align-self="center">
          <safa-icon />
          Sorry, an error has occurred please refresh your browser and try
          again.
        </v-col>
      </v-row>
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { PrivatePage, SafaIcon } from "@/components";

/**
 * The default page displayed if an unknown error is encountered.
 */
export default Vue.extend({
  components: {
    SafaIcon,
    PrivatePage,
  },
});
</script>
