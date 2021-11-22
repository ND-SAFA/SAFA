import { TraceApproval, TraceLink } from "@/types";
import { appModule, projectModule } from "@/store";
import { approveLink, declineLink } from "@/api/endpoints";

/**
 * Processes link approvals, setting the app state to loading in between, and updating trace links afterwards.
 *
 * @param link - The trace link to process.
 * @param onSuccess - Run when the API call successfully resolves.
 */
export function approveLinkAPIHandler(
  link: TraceLink,
  onSuccess?: () => void
): void {
  link.approvalStatus = TraceApproval.APPROVED;

  linkAPIHandler(link, approveLink, () => {
    if (onSuccess !== undefined) {
      onSuccess();
    }

    projectModule.addOrUpdateTraceLinks([link]);
  });
}

/**
 * Processes link declines, setting the app state to loading in between, and updating trace links afterwards.
 *
 * @param link - The trace link to process.
 * @param onSuccess - Run when the API call successfully resolves.
 */
export function declineLinkAPIHandler(
  link: TraceLink,
  onSuccess?: () => void
): void {
  link.approvalStatus = TraceApproval.DECLINED;

  linkAPIHandler(link, declineLink, () => {
    if (onSuccess !== undefined) {
      onSuccess();
    }

    projectModule.removeTraceLink(link);
  });
}

/**
 * Processes link API functions, setting the app state to loading in between.
 *
 * @param link - The trace link to process.
 * @param linkAPI - The endpoint to call with the link.
 * @param onSuccess - Run when the API call successfully resolves.
 */
export function linkAPIHandler(
  link: TraceLink,
  linkAPI: (traceLink: TraceLink) => Promise<void>,
  onSuccess: () => void
): void {
  appModule.onLoadStart();
  linkAPI(link).then(onSuccess).finally(appModule.onLoadEnd);
}
