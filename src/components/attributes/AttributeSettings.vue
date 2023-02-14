<template>
  <panel-card>
    <v-row style="min-height: 60vh">
      <v-col cols="12" lg="4">
        <v-navigation-drawer
          v-if="$vuetify.breakpoint.lgAndUp"
          absolute
          permanent
          width="33%"
        >
          <attribute-editor />
        </v-navigation-drawer>
        <attribute-editor v-else />
      </v-col>
      <v-col cols="12" lg="8">
        <attribute-layout-editor />
      </v-col>
    </v-row>
  </panel-card>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { PanelCard } from "@/components/common";
import AttributeEditor from "./AttributeEditor.vue";
import AttributeLayoutEditor from "./AttributeLayoutEditor.vue";

/**
 * Renders settings for customizing artifact attributes.
 */
export default defineComponent({
  name: "AttributeSettings",
  components: {
    AttributeLayoutEditor,
    AttributeEditor,
    PanelCard,
  },
});
</script>
