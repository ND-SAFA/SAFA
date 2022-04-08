<template>
  <v-menu offset-y left :close-on-content-click="false">
    <template v-slot:activator="{ on: menuOn }">
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            v-on="{ ...menuOn, ...on }"
            v-bind="attrs"
            color="secondary"
            icon
            :disabled="isDisabled"
          >
            <v-icon>{{ definition.icon }}</v-icon>
          </v-btn>
        </template>
        <span>{{ definition.label }}</span>
      </v-tooltip>
    </template>
    <v-list>
      <v-hover
        v-slot:default="{ hover }"
        v-for="(item, itemIndex) in definition.menuItems"
        :key="item.name"
      >
        <v-list-item :style="hover ? `background-color: ${hoverColor};` : ''">
          <v-checkbox
            readonly
            :label="item.name"
            :input-value="definition.checkmarkValues[itemIndex]"
            @click.stop="item.onClick"
          />
        </v-list-item>
      </v-hover>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import { ButtonDefinition } from "@/types";
import Vue, { PropType } from "vue";
import { ThemeColors } from "@/util";

export default Vue.extend({
  props: {
    definition: Object as PropType<ButtonDefinition>,
    isDisabled: Boolean,
  },
  data() {
    return {
      hoverColor: ThemeColors.menuHighlight,
    };
  },
});
</script>
