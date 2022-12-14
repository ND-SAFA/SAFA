<template>
  <panel-card>
    <v-row>
      <v-col cols="4">
        <attribute-editor />
      </v-col>
      <v-col cols="8">
        <attribute-layout-editor />
      </v-col>
    </v-row>
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { PanelCard } from "@/components/common";
import AttributeEditor from "./AttributeEditor.vue";
import AttributeLayoutEditor from "./AttributeLayoutEditor.vue";

/**
 * Renders settings for customizing artifact attributes.
 */
export default Vue.extend({
  name: "AttributeSettings",
  components: {
    AttributeLayoutEditor,
    AttributeEditor,
    PanelCard,
  },
});
</script>
