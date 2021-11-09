<template>
  <v-menu offset-y left :close-on-content-click="false">
    <template v-slot:activator="{ on }">
      <v-btn icon small color="secondary" dark v-on="on">
        <v-icon>{{ definition.icon }}</v-icon>
      </v-btn>
    </template>
    <v-list>
      <v-hover
        v-slot:default="{ hover }"
        v-for="(item, itemIndex) in definition.menuItems"
        :key="item"
      >
        <v-list-item :style="hover ? `background-color: ${hoverColor};` : ''">
          <v-checkbox
            readonly
            :label="item"
            :input-value="definition.checkmarkValues[itemIndex]"
            @click="(newState) => definition.menuHandlers[itemIndex](newState)"
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
  },
  data() {
    return {
      hoverColor: ThemeColors.menuHighlight,
    };
  },
});
</script>
