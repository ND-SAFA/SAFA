<template>
  <v-menu offset-y left :close-on-content-click="false">
    <template #activator="{ props: menuProps }">
      <v-tooltip bottom>
        <template #activator="{ props }">
          <v-btn
            v-bind="{ ...menuProps, ...props }"
            color="accent"
            icon
            :data-cy="definition.dataCy"
            :class="isDisabled ? 'disable-events' : ''"
          >
            <v-icon>{{ definition.icon }}</v-icon>
          </v-btn>
        </template>
        <span>{{ definition.label }}</span>
      </v-tooltip>
    </template>
    <v-list>
      <v-hover
        v-for="(item, itemIndex) in definition.menuItems"
        v-slot="{ hover }"
        :key="item.name"
      >
        <v-list-item
          :style="hover ? `background-color: ${hoverColor};` : ''"
          data-cy="button-checkmark-menu-item"
          @click.stop="item.onClick"
        >
          <v-checkbox
            readonly
            :label="item.name"
            :input-value="definition.checkmarkValues[itemIndex]"
          />
        </v-list-item>
      </v-hover>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ButtonDefinition } from "@/types";
import { ThemeColors } from "@/util";

/**
 * Renders a checkbox dropdown menu.
 */
export default Vue.extend({
  name: "CheckmarkMenu",
  props: {
    definition: Object as PropType<ButtonDefinition>,
    isDisabled: Boolean,
  },
  data() {
    return {
      hoverColor: ThemeColors.lightGrey,
    };
  },
});
</script>
