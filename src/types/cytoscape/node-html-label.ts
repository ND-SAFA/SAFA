import { ArtifactData } from "@/types/domain/artifact";

type HorizontalAlignment = "center" | "left" | "right";
type VerticalAlignment = "center" | "top" | "bottom";
type HtmlDefinitionFunction = (data: ArtifactData) => string;

export interface HtmlDefinition {
  query: string;
  halign: HorizontalAlignment;
  valign: VerticalAlignment;
  halignBox: HorizontalAlignment;
  valignBox: VerticalAlignment;
  tpl: HtmlDefinitionFunction;
}
