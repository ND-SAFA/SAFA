import SockJS from "sockjs-client";
import Stomp, { Client, Frame } from "webstomp-client";
import { getProjectVersion } from "@/api/project-api";
import { Update } from "@/types";
import { appModule, projectModule } from "@/store";
import { baseURL } from "@/api/base-url";

const WEBSOCKET_URL = `${baseURL}/websocket`;
let sock: WebSocket;
let stompClient: Client;

let recInterval: NodeJS.Timeout;
let currentReconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 20;
const RECONNECT_WAIT_TIME = 5000;

function getStompClient(reconnect = false): Client {
  if (sock === undefined || stompClient === undefined || reconnect) {
    try {
      sock = new SockJS(WEBSOCKET_URL, { DEBUG: false });
      sock.onclose = () => {
        console.log("web socket close");
        connect().then();
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

function connect(isReconnect = false): Promise<void> {
  return new Promise((resolve, reject) => {
    const stomp = getStompClient(isReconnect);
    if (stomp.connected) {
      console.log("already connected!");
      clearInterval(recInterval);
      resolve();
    }

    console.log("web socket connection attempt:", currentReconnectAttempts);
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
          if (currentReconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
            connect(true).then(resolve).catch(reject);
          } else {
            clearInterval(recInterval);
            reject(
              "Reached max web socket reconnect attempts, please reload page."
            );
          }
        }, RECONNECT_WAIT_TIME);
      }
    );
  });
}

function clearSubscriptions() {
  const stomp = getStompClient();
  const subscriptionIds = Object.keys(stomp.subscriptions);
  subscriptionIds.forEach((subId) => stomp.unsubscribe(subId));
}

export function connectAndSubscriptToVersion(
  projectId: string,
  versionId: string
): Promise<void> {
  return new Promise((resolve, reject) => {
    connect()
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
