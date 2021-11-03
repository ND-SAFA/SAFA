export interface LinkType {
  source: string;
  target: string;
}

export enum TraceApproval {
  UNREVIEWED = "UNREVIEWED",
  APPROVED = "APPROVED",
  DECLINED = "DECLINED",
}

export enum TraceType {
  GENERATED = "GENERATED",
  MANUAL = "MANUAL",
}

export interface Link {
  source: string;
  target: string;
}

export interface TraceLink extends Link {
  traceLinkId: string;
  approvalStatus: TraceApproval;
  score: number;
  traceType: TraceType;
}

export interface TraceLinkDisplayData extends TraceLink {
  sourceBody: string;
  targetBody: string;
}
