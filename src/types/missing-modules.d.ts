declare module "cytoscape-node-html-label";
declare module "cytoscape-klay";
declare module "cytoscape-automove";
declare module "cytoscape-context-menus";
declare module "cytoscape-edgehandles";

declare module "vue" {
  import { CompatVue } from "@vue/runtime-dom";
  const Vue: CompatVue;
  export default Vue;
  export * from "@vue/runtime-dom";
  const { configureCompat } = Vue;
  export { configureCompat };
}

declare module "vue-grid-layout" {
  import { defineComponent } from "vue";

  export class GridLayout extends Vue {}

  export class GridItem extends Vue {}

  export interface GridItemData {
    x: number;
    y: number;
    w: number;
    h: number;
    i: string;
  }
}
