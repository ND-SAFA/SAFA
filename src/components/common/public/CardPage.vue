<template>
  <v-main :class="className">
    <v-container class="fill-height">
      <v-card rounded elevation="2" class="mx-auto py-4 px-6" width="30em">
        <v-card-title class="mx-auto width-max my-2">
          <safa-icon style="width: 14em" />
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
import { SafaIcon } from "@/components/common/display";

/**
 * Presents the page within a card containing SAFA title, a slot for a form,
 * and a slot for its actions.
 */
export default Vue.extend({
  name: "CardPage",
  components: { SafaIcon },
  computed: {
    /**
     * @return The page's class name.
     */
    className(): string {
      return this.$vuetify.theme.dark
        ? "neutral-bg fill-height"
        : "primary fill-height";
    },
  },
});
</script>
