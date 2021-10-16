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

export interface TraceLink {
  traceLinkId: string;
  source: string;
  target: string;
  approvalStatus: TraceApproval;
  score: number;
  traceType: TraceType;
}

export interface TraceLinkDisplayData extends TraceLink {
  sourceBody: string;
  targetBody: string;
}
