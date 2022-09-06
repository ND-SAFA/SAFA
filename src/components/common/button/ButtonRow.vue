<template>
  <flex-box>
    <template v-for="definition in definitions">
      <icon-button
        v-if="!definition.isHidden && definition.type === iconType"
        :key="definition.label"
        :definition="definition"
      />
      <checkmark-menu
        v-else-if="
          !definition.isHidden && definition.type === checkmarkMenuType
        "
        :key="definition.label"
        :definition="definition"
      />
      <list-menu
        v-else-if="!definition.isHidden && definition.type === listMenuType"
        :key="definition.label"
        :definition="definition"
      />
    </template>
  </flex-box>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ButtonDefinition, ButtonType } from "@/types";
import { FlexBox } from "@/components/common/display";
import IconButton from "./IconButton.vue";
import CheckmarkMenu from "./CheckmarkMenu.vue";
import ListMenu from "./ListMenu.vue";

/**
 * Renders a generic row of buttons.
 */
export default Vue.extend({
  name: "ButtonRow",
  components: { FlexBox, IconButton, CheckmarkMenu, ListMenu },
  props: {
    definitions: Array as PropType<ButtonDefinition[]>,
    large: Boolean,
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
