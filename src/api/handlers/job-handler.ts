import { Job } from "@/types";
import { connectAndSubscribeToJob } from "@/api";

/**
 * Subscribes to job updates via websocket messages. Job updates
 * are automatically processed in the job module.
 * @param job The job to be subscribed to.
 */
export async function handleJobSubmission(job: Job): Promise<void> {
  await connectAndSubscribeToJob(job.id);
}
