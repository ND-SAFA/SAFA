/**
 * The methods of alignment.
 */
export type AlignType = "start" | "center" | "end";

/**
 * The methods of justifying.
 */
export type JustifyType = AlignType | "between" | "around";

export type ThemeColor =
  | "primary"
  | "secondary"
  | "accent"
  | "positive"
  | "negative"
  | "nodeDefault"
  | "nodeGenerated"
  | string;
