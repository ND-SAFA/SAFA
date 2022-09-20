import { LayoutPositionsModel } from "@/types";

/**
 * Represents the configuration to refresh document layouts.
 */
export interface LayoutRegenerationModel {
  /**
   * If true, the default document will be regenerated.
   */
  defaultDocument: boolean;
  /**
   * A list of all document ids to regenerate.
   */
  documentIds: string[];
}

/**
 * Represents regenerated layouts.
 */
export interface GeneratedLayoutsModel {
  /**
   * Returns the layout for the default document.
   */
  defaultDocumentLayout: LayoutPositionsModel;
  /**
   * Returns the layout for each document regenerated, keyed by document id.
   */
  documentLayoutMap: Record<string, LayoutPositionsModel>;
}
