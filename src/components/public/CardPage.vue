<template>
  <v-main class="primary fill-height">
    <v-container class="fill-height">
      <v-card rounded elevation="2" class="mx-auto py-4 px-6" width="30em">
        <v-card-title style="width: max-content" class="mx-auto">
          <safa-icon />
          <h1 class="text-h2 font-weight-bold primary-text">SAFA</h1>
        </v-card-title>

        <v-form class="px-2">
          <slot name="form" />
        </v-form>

        <v-card-actions>
          <slot name="actions" />
        </v-card-actions>
      </v-card>
    </v-container>
  </v-main>
</template>

<script lang="ts">
import Vue from "vue";
import { SafaIcon } from "@/components/navigation";

/**
 * Presents the login page.
 */
export default Vue.extend({
  name: "card-page",
  components: { SafaIcon },
});
</script>
