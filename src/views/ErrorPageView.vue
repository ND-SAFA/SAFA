<template>
  <v-container>
    <v-row justify="center">
      <v-col align-self="center">
        <safa-icon />
        Sorry, an error has occurred please refresh your broswer and try again.
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import SafaIcon from "@/components/navigation/SafaIcon.vue";

export default Vue.extend({
  components: {
    SafaIcon,
  },
});
</script>
