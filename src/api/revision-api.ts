import SockJS from "sockjs-client";
import Stomp, { Client, Frame } from "webstomp-client";
import { getProjectVersion } from "@/api/project-api";
import { ProjectVersionUpdate } from "@/types";
import { appModule, projectModule } from "@/store";
import { baseURL } from "@/api/endpoints";

const WEBSOCKET_URL = `${baseURL}/websocket`;
let sock: WebSocket;
let stompClient: Client;

const MAX_RECONNECT_ATTEMPTS = 20;
const RECONNECT_WAIT_TIME = 5000;
let recInterval: NodeJS.Timeout;
let currentReconnectAttempts = 0;

/**
 * Returns singleton Stomp client or create new one if undefined.
 *
 * @param reconnect - Whether to create a new connection regardless
 * of websocket state.
 * @throws Throws errors if can't connect to server and reconnect is
 * not enabled.
 * @return The stomp client.
 */
function getStompClient(reconnect = false): Client {
  if (sock === undefined || stompClient === undefined || reconnect) {
    try {
      sock = new SockJS(WEBSOCKET_URL, { DEBUG: false });
      sock.onclose = () => {
        console.log("web socket close");
        connect(MAX_RECONNECT_ATTEMPTS, RECONNECT_WAIT_TIME).then();
      };
      stompClient = Stomp.over(sock, { debug: false });
    } catch (e) {
      if (!reconnect) {
        throw e;
      }
    }
  }
  return stompClient;
}

/**
 * Connects to BEND websocket with a Stomp protocol and tries to reconnect if
 * the connection fails.
 *
 * @param maxReconnectAttempts - The number of times to try to reconnect before
 * failing.
 * @param reconnectWaitTime - The number of milliseconds to wait before attempting
 * reconnect
 * @param isReconnect - Whether this is a reconnect attempt.
 */
function connect(
  maxReconnectAttempts: number,
  reconnectWaitTime: number,
  isReconnect = false
): Promise<void> {
  return new Promise((resolve, reject) => {
    const stomp = getStompClient(isReconnect);
    if (stomp.connected) {
      console.log("already connected!");
      clearInterval(recInterval);
      resolve();
    }

    if (currentReconnectAttempts > 0) {
      console.log("web socket reconnect attempt:", currentReconnectAttempts);
    }

    currentReconnectAttempts++;
    stomp.connect(
      { host: WEBSOCKET_URL },
      () => {
        if (currentReconnectAttempts > 1) {
          appModule.onSuccess("Web Socket reconnected to server.");
        }
        console.log("connection successful");
        clearInterval(recInterval);
        currentReconnectAttempts = 0;
        resolve();
      },
      () => {
        console.log("attempting re-connect!");
        if (!isReconnect) {
          appModule.onError("Web Socket lost connection to server.");
        }
        clearInterval(recInterval);
        recInterval = setInterval(function () {
          if (currentReconnectAttempts < maxReconnectAttempts) {
            connect(maxReconnectAttempts, reconnectWaitTime, true)
              .then(resolve)
              .catch(reject);
          } else {
            clearInterval(recInterval);
            const error =
              "Reached max web socket reconnect attempts, please reload page.";
            appModule.onError(error);
            reject(error);
          }
        }, reconnectWaitTime);
      }
    );
  });
}

/**
 * Clears all stomp client subscriptions.
 */
function clearSubscriptions() {
  const stomp = getStompClient();
  const subscriptionIds = Object.keys(stomp.subscriptions);

  subscriptionIds.forEach((subId) => stomp.unsubscribe(subId));
}

/**
 * Connects and subscribes to the given project and version.
 *
 * @param projectId - The project ID to connect to.
 * @param versionId - The project version ID to connect to.
 */
export function connectAndSubscribeToVersion(
  projectId: string,
  versionId: string
): Promise<void> {
  return new Promise((resolve, reject) => {
    connect(MAX_RECONNECT_ATTEMPTS, RECONNECT_WAIT_TIME)
      .then(() => {
        clearSubscriptions();
        const projectSubscription = `/topic/projects/${projectId}`;
        const versionSubscription = `/topic/revisions/${versionId}`;
        stompClient.subscribe(projectSubscription, (frame) =>
          revisionMessageHandler(versionId, frame)
        );
        stompClient.subscribe(versionSubscription, (frame) =>
          revisionMessageHandler(versionId, frame)
        );
        resolve();
      })
      .catch(reject);
  });
}

/**
 * Handles revision messages.
 *
 * @param versionId - The project version ID of the revision.
 * @param frame - The frame of the revision.
 */
function revisionMessageHandler(versionId: string, frame: Frame): void {
  const revision: ProjectVersionUpdate = JSON.parse(
    frame.body
  ) as ProjectVersionUpdate;

  switch (revision.type) {
    case "included":
      projectModule.addOrUpdateArtifacts(revision.artifacts);
      projectModule.addOrUpdateTraceLinks(revision.traces);
      break;
    case "excluded":
      getProjectVersion(versionId).then(
        projectModule.setProjectCreationResponse
      );
  }
}

connect(MAX_RECONNECT_ATTEMPTS, RECONNECT_WAIT_TIME).then();
