<template>
  <div class="ma-8">
    <slot name="header" />
    <v-row dense>
      <v-col :cols="$vuetify.breakpoint.lgAndUp ? 4 : 12">
        <slot name="sidebar" />
      </v-col>
      <v-col :cols="$vuetify.breakpoint.lgAndUp ? 8 : 12">
        <slot />
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

/**
 * Represents a grid with a sidebar that changes
 * to a stacked representation at smaller screen sizes.
 */
export default Vue.extend({
  name: "SidebarGrid",
});
</script>
