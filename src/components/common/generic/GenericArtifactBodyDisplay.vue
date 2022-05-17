<template>
  <v-list-item-content style="max-width: 500px">
    <v-list-item-title v-if="!!title" v-html="title" />
    <v-list-item-subtitle v-if="!isExpanded" v-html="body" />
    <v-list-item-content v-if="isExpanded" v-html="body" />
    <v-list-item-action class="ma-0 pt-1">
      <v-spacer />
      <v-btn text small @click.stop="isExpanded = !isExpanded">
        {{ isExpanded ? "See Less" : "See More" }}
      </v-btn>
    </v-list-item-action>
  </v-list-item-content>
</template>

<script lang="ts">
import Vue from "vue";

/**
 * Displays the body of an artifact that can be expanded.
 */
export default Vue.extend({
  name: "GenericArtifactBodyDisplay",
  props: {
    title: {
      type: String,
      required: false,
    },
    body: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      isExpanded: false,
    };
  },
});
</script>
