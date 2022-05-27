import {
  clearSubscriptions,
  connect,
  Endpoint,
  fillEndpoint,
  stompClient,
} from "@/api";
import { Frame } from "webstomp-client";
import { Job } from "@/types";
import { jobModule, logModule } from "@/store";

/**
 * Subscribes to updates for job with given id.
 * @param jobId The id for the job whose updates we want to process.
 */
export function connectAndSubscribeToJob(jobId: string): Promise<void> {
  return new Promise((resolve) => {
    if (!jobId) {
      resolve();
      return;
    }
    connect().then(() => {
      //clearSubscriptions();
      stompClient.subscribe(
        fillEndpoint(Endpoint.listenForJob, { jobId }),
        jobMessageHandler
      );
      resolve();
    });
  });
}

/**
 * Adds or Updates incoming job entities in the JobModule.
 * @param frame Incoming websocket frame
 */
function jobMessageHandler(frame: Frame): void {
  const incomingJob: Job = JSON.parse(frame.body) as Job;
  jobModule.addOrUpdateJob(incomingJob);
  logModule.onDevMessage(`New Job message: ${incomingJob}`);
}
