<template>
  <v-row class="ma-0 pa-0">
    <v-col
      v-for="definition in definitions"
      :key="definition.label"
      :cols="12 / definitions.length"
    >
      <v-row :justify="justify">
        <IconButtonItem
          v-if="definition.type === iconType"
          :definition="definition"
        />
        <CheckmarkMenuItem
          v-else-if="definition.type === checkmarkMenuType"
          :definition="definition"
        />
        <ListMenu
          v-else-if="definition.type === listMenuType"
          :definition="definition"
        />
      </v-row>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ButtonDefinition, ButtonType } from "@/types/common-components";
import IconButtonItem from "@/components/common/button-row/IconButton.vue";
import CheckmarkMenuItem from "@/components/common/button-row/CheckmarkMenu.vue";
import ListMenu from "@/components/common/button-row/ListMenu.vue";

export default Vue.extend({
  components: { IconButtonItem, CheckmarkMenuItem, ListMenu },
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
