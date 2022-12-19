import { LayoutPositionsSchema } from "@/types";

/**
 * Represents the configuration to refresh document layouts.
 */
export interface LayoutRegenerationSchema {
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
export interface GeneratedLayoutsSchema {
  /**
   * Returns the layout for the default document.
   */
  defaultDocumentLayout: LayoutPositionsSchema;
  /**
   * Returns the layout for each document regenerated, keyed by document id.
   */
  documentLayoutMap: Record<string, LayoutPositionsSchema>;
}
