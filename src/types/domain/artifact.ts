import { ArtifactDeltaState } from "@/types/domain/delta";

export interface Artifact {
  name: string;
  summary?: string;
  body: string;
  type: string;
}

export interface TraceDefinition {
  source: string;
  target: string;
}

export interface ArtifactData {
  id: string;
  body: string;
  type: string;
  warnings?: ArtifactWarning[];
  artifactName: string;
  artifactType: string;
  artifactDeltaState: ArtifactDeltaState;
  isSelected: boolean;
  opacity: number;
}

export interface ArtifactWarning {
  ruleName: string;
  ruleMessage: string;
}

export type ProjectWarnings = Record<string, ArtifactWarning[]>;
