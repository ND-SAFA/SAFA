<template>
  <v-row class="ma-0 pa-0">
    <v-col
      v-for="definition in definitions"
      :key="definition.label"
      :cols="12 / definitions.length"
    >
      <v-row :justify="justify">
        <icon-button
          v-if="!definition.isHidden && definition.type === iconType"
          :definition="definition"
        />
        <checkmark-menu
          v-else-if="
            !definition.isHidden && definition.type === checkmarkMenuType
          "
          :definition="definition"
        />
        <list-menu
          v-else-if="!definition.isHidden && definition.type === listMenuType"
          :definition="definition"
        />
      </v-row>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ButtonDefinition, ButtonType } from "@/types";
import IconButton from "./IconButton.vue";
import CheckmarkMenu from "./CheckmarkMenu.vue";
import ListMenu from "./ListMenu.vue";

/**
 * Renders a generic row of buttons.
 */
export default Vue.extend({
  name: "ButtonRow",
  components: { IconButton, CheckmarkMenu, ListMenu },
  props: {
    definitions: Array as PropType<ButtonDefinition[]>,
    justify: {
      type: String,
      required: false,
      default: "center",
    },
  },
  data() {
    return {
      iconType: ButtonType.ICON,
      checkmarkMenuType: ButtonType.CHECKMARK_MENU,
      listMenuType: ButtonType.LIST_MENU,
    };
  },
});
</script>
