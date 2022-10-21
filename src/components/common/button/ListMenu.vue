<template>
  <v-menu offset-y bottom :rounded="false">
    <template v-slot:activator="{ on }">
      <v-btn
        :outlined="!buttonIsText"
        :text="buttonIsText"
        :color="buttonColor"
        v-on="on"
        :disabled="disabled"
        :data-cy="definition.dataCy"
      >
        <v-icon>mdi-chevron-down</v-icon>
        {{ buttonLabel }}
      </v-btn>
    </template>
    <v-list>
      <v-container
        v-for="(item, itemIndex) in definition.menuItems"
        :key="item.name"
        class="mt-0 mb-0 pt-0 pb-0"
      >
        <v-tooltip
          bottom
          open-delay="300"
          z-index="12"
          :disabled="!item.tooltip"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              v-on="on"
              v-bind="attrs"
              text
              block
              class="text-none"
              :color="itemColor"
              @click="() => onItemClick(itemIndex, item.name)"
            >
              {{ item.name }}
            </v-btn>
          </template>
          <span>{{ item.tooltip }}</span>
        </v-tooltip>
      </v-container>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ListMenuDefinition } from "@/types";
import { ThemeColors } from "@/util";

/**
 * Renders a list menu.
 */
export default Vue.extend({
  name: "ListMenu",
  props: {
    definition: {
      type: Object as PropType<ListMenuDefinition>,
      required: true,
    },
  },
  data() {
    return {
      hover: true,
      hoverColor: ThemeColors.lightGrey,
    };
  },
  computed: {
    /**
     * @return The currently selected value.
     */
    selectedValue(): string {
      return this.definition.selectedItem || "";
    },
    /**
     * @return Whether the menu is disabled.
     */
    disabled(): boolean {
      return this.definition.isDisabled !== undefined
        ? this.definition.isDisabled
        : false;
    },
    /**
     * @return The button color.
     */
    buttonColor(): string {
      return this.definition.buttonColor || "accent";
    },
    /**
     * @return The item color.
     */
    itemColor(): string {
      return this.definition.itemColor || "primary";
    },
    /**
     * @return Whether this is a text button.
     */
    buttonIsText(): boolean {
      const { buttonIsText } = this.definition;
      return buttonIsText === undefined ? true : buttonIsText;
    },
    /**
     * @return Whether to show the selected value.
     */
    showSelectedValue(): boolean {
      const { showSelectedValue } = this.definition;
      return showSelectedValue === undefined ? false : showSelectedValue;
    },
    /**
     * @return The button label.
     */
    buttonLabel(): string {
      if (this.showSelectedValue && this.selectedValue !== "") {
        return this.selectedValue;
      }
      return this.definition.label;
    },
  },
  methods: {
    /**
     * When an item is clicked, the value will be selected, and the on click callback will be run.
     */
    onItemClick(itemIndex: number, value: string): void {
      this.definition.menuItems?.[itemIndex].onClick();
      this.definition.selectedItem = value;
    },
  },
});
</script>
