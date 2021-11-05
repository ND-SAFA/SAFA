import { TraceApproval, TraceLink } from "@/types";
import { appModule, projectModule } from "@/store";
import { approveLink, declineLink } from "@/api/link-api";

export function linkAPIHandler(
  link: TraceLink,
  linkAPI: (traceLinkId: string) => Promise<void>,
  onSuccess: () => void
): void {
  appModule.onLoadStart();
  linkAPI(link.traceLinkId).then(onSuccess).finally(appModule.onLoadEnd);
}

export function approveLinkAPIHandler(
  link: TraceLink,
  onSuccess: (() => void) | undefined
): void {
  link.approvalStatus = TraceApproval.APPROVED;
  linkAPIHandler(link, approveLink, () => {
    if (onSuccess !== undefined) {
      onSuccess();
    }
    projectModule.addOrUpdateTraceLinks([link]);
  });
}

export function declineLinkAPIHandler(
  link: TraceLink,
  onSuccess: (() => void) | undefined
): void {
  link.approvalStatus = TraceApproval.DECLINED;
  linkAPIHandler(link, declineLink, () => {
    if (onSuccess !== undefined) {
      onSuccess();
    }
    projectModule.removeTraceLink(link);
  });
}
