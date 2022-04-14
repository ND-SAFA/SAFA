import { EmptyLambda, TraceApproval, TraceLink } from "@/types";
import { appModule, logModule, projectModule } from "@/store";
import {
  createLink,
  updateApprovedLink,
  updateDeclinedLink,
} from "@/api/commits";

/**
 * Creates a new trace link.
 *
 * @param link - The trace link to process.
 */
export async function handleCreateLink(link: TraceLink): Promise<void> {
  try {
    const createdLinks = await createLink(link);

    await projectModule.addOrUpdateTraceLinks(createdLinks);
  } catch (e) {
    logModule.onError("Unable to create trace link");
    logModule.onDevError(e.toString());
  }
}

/**
 * Processes link approvals, setting the app state to loading in between, and updating trace links afterwards.
 *
 * @param link - The trace link to process.
 * @param onSuccess - Run when the API call successfully resolves.
 */
export async function handleApproveLink(
  link: TraceLink,
  onSuccess?: EmptyLambda
): Promise<void> {
  link.approvalStatus = TraceApproval.APPROVED;

  linkAPIHandler(link, updateApprovedLink, async () => {
    onSuccess?.();

    await projectModule.addOrUpdateTraceLinks([link]);
  });
}

/**
 * Processes link declines, setting the app state to loading in between, and updating trace links afterwards.
 *
 * @param link - The trace link to process.
 * @param onSuccess - Run when the API call successfully resolves.
 */
export async function handleDeclineLink(
  link: TraceLink,
  onSuccess?: EmptyLambda
): Promise<void> {
  link.approvalStatus = TraceApproval.DECLINED;

  linkAPIHandler(link, updateDeclinedLink, async () => {
    onSuccess?.();

    await projectModule.deleteTraceLinks([link]);
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
  linkAPI: (traceLink: TraceLink) => Promise<TraceLink[]>,
  onSuccess: () => Promise<void>
): void {
  appModule.onLoadStart();
  linkAPI(link).then(onSuccess).finally(appModule.onLoadEnd);
}
