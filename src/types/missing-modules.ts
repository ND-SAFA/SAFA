declare module "cytoscape-node-html-label";
declare module "cytoscape-klay";
declare module "cytoscape-automove";
declare module "cytoscape-context-menus";
declare module "cytoscape-edgehandles";

declare module "vue-grid-layout" {
  import Vue from "vue";

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
