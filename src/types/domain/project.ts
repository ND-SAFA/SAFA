import { TraceLink } from "@/types/domain/links";
import { Artifact } from "@/types/domain/artifact";

export enum ApplicationActivity {
  PARSING_TIM,
  PARSING_ARTIFACTS,
  PARSING_TRACES,
  UNKNOWN,
}

export interface ParserError {
  errorId: string;
  message: string;
  activity: ApplicationActivity;
  location: string;
}

export interface ProjectErrors {
  tim: ParserError[];
  artifacts: ParserError[];
  traces: ParserError[];
}

export interface ProjectIdentifier {
  projectId: string;
  name: string;
  description: string;
}

export interface ProjectVersion {
  versionId: string;
  project?: ProjectIdentifier;
  majorVersion: number;
  minorVersion: number;
  revision: number;
}

export interface Project extends ProjectIdentifier {
  projectVersion?: ProjectVersion;
  artifacts: Artifact[];
  traces: TraceLink[];
}
