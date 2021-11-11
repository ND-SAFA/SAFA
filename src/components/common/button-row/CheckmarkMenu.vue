<template>
  <v-menu offset-y left :close-on-content-click="false">
    <template v-slot:activator="{ on }">
      <generic-icon-button
        v-on="on"
        color="secondary"
        :tooltip="definition.label"
        :icon-id="definition.icon"
      />
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
import { GenericIconButton } from "@/components/common/generic";

export default Vue.extend({
  components: {
    GenericIconButton,
  },
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
