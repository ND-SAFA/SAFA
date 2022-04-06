<template>
  <v-menu offset-y left :close-on-content-click="false">
    <template v-slot:activator="{ on }">
      <v-btn icon small color="secondary" dark v-on="on">
        <v-icon>mdi-filter</v-icon>
      </v-btn>
    </template>
    <v-list>
      <v-list-item v-for="item in artifactTypes" :key="item">
        <v-checkbox :label="item" :value="item" v-model="selectedMenuItems" />
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import { typeOptionsModule } from "@/store";
import Vue from "vue";

export default Vue.extend({
  computed: {
    data() {
      return {
        selectedMenuItems: [],
      };
    },
    artifactTypes(): string[] {
      return typeOptionsModule.artifactTypes;
    },
  },
});
</script>
