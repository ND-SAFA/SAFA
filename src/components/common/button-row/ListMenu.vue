<template>
  <v-menu offset-y bottom :rounded="false">
    <template v-slot:activator="{ on }">
      <v-btn
        :text="buttonIsText"
        small
        :color="buttonColor"
        v-on="on"
        :disabled="disabled"
      >
        {{ buttonLabel }}
      </v-btn>
    </template>
    <v-list>
      <v-container
        v-for="(item, itemIndex) in definition.menuItems"
        :key="item"
        class="mt-0 mb-0 pt-0 pb-0"
      >
        <v-btn
          text
          class="text-none"
          :color="itemColor"
          @click="() => onItemClick(itemIndex, item)"
          >{{ item }}</v-btn
        >
      </v-container>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ListMenuDefinition } from "@/types";
import { ThemeColors } from "@/util";

const DEFAULT_BUTTON_COLOR = "secondary";
const DEFAULT_ITEM_COLOR = "primary";
const DEFAULT_BUTTON_IS_TEXT = true;
const DEFAULT_SHOW_SELECTED_VALUE = false;

export default Vue.extend({
  props: {
    definition: {
      type: Object as PropType<ListMenuDefinition>,
      required: true,
    },
  },
  data() {
    return {
      hover: true,
      hoverColor: ThemeColors.menuHighlight,
      selectedValue: "",
    };
  },
  computed: {
    disabled(): boolean {
      return this.definition.isDisabled !== undefined
        ? this.definition.isDisabled
        : false;
    },
    buttonColor(): string {
      const { buttonColor } = this.definition;
      return buttonColor === undefined ? DEFAULT_BUTTON_COLOR : buttonColor;
    },
    itemColor(): string {
      const { itemColor } = this.definition;
      return itemColor === undefined ? DEFAULT_ITEM_COLOR : itemColor;
    },
    buttonIsText(): boolean {
      const { buttonIsText } = this.definition;
      return buttonIsText === undefined ? DEFAULT_BUTTON_IS_TEXT : buttonIsText;
    },
    showSelectedValue(): boolean {
      const { showSelectedValue } = this.definition;
      return showSelectedValue === undefined
        ? DEFAULT_SHOW_SELECTED_VALUE
        : showSelectedValue;
    },
    buttonLabel(): string {
      if (this.showSelectedValue && this.selectedValue !== "") {
        return this.selectedValue;
      }
      return this.definition.label;
    },
  },
  methods: {
    onItemClick(itemIndex: number, value: string): void {
      this.$props.definition.menuHandlers[itemIndex]("payload");
      this.selectedValue = value;
    },
  },
});
</script>
