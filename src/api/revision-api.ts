import SockJS from "sockjs-client";
import Stomp, { Frame } from "webstomp-client";
import { getProjectVersion } from "@/api/project-api";
import { Update } from "@/types/api";
import { projectModule } from "@/store";
import { baseURL } from "@/api/base-url";

const WEBSOCKET_URL = `${baseURL}/websocket`;

const sock = new SockJS(WEBSOCKET_URL, { DEBUG: false });
const stompClient = Stomp.over(sock, { debug: false });

function connect() {
  stompClient.connect(
    { host: WEBSOCKET_URL },
    (frame) => console.log("ON CONNECT CALLED!", frame),
    (e) => console.log("ERROR CONNECTING TO WEBSOCKET:", e)
  );
}

function clearSubscriptions() {
  const subscriptionIds = Object.keys(stompClient.subscriptions);
  subscriptionIds.forEach((subId) => stompClient.unsubscribe(subId));
}

export function connectAndSubscriptToVersion(
  projectId: string,
  versionId: string
): void {
  if (!stompClient.connected) {
    connect();
  }
  clearSubscriptions();
  const projectSubscription = `/topic/projects/${projectId}`;
  const versionSubscription = `/topic/revisions/${versionId}`;
  stompClient.subscribe(projectSubscription, (frame) =>
    revisionMessageHandler(versionId, frame)
  );
  stompClient.subscribe(versionSubscription, (frame) =>
    revisionMessageHandler(versionId, frame)
  );
}

function revisionMessageHandler(versionId: string, frame: Frame): void {
  const revision: Update = JSON.parse(frame.body) as Update;

  switch (revision.type) {
    case "included":
      projectModule.addOrUpdateArtifacts(revision.artifacts);
      projectModule.addOrUpdateTraceLinks(revision.traces);
      break;
    case "excluded":
      getProjectVersion(versionId).then(async (projectCreationResponse) => {
        await projectModule.setProjectCreationResponse(projectCreationResponse);
      });
  }
}

connect();
