package edu.nd.crc.safa.test.services.notifications;

import static java.util.concurrent.TimeUnit.SECONDS;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.LinkedBlockingDeque;

import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.config.WebSocketBrokerConfig;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.jetbrains.annotations.NotNull;
import org.springframework.messaging.simp.stomp.StompFrameHandler;
import org.springframework.messaging.simp.stomp.StompHeaders;
import org.springframework.messaging.simp.stomp.StompSession;
import org.springframework.messaging.simp.stomp.StompSessionHandlerAdapter;
import org.springframework.web.socket.WebSocketHttpHeaders;
import org.springframework.web.socket.client.standard.StandardWebSocketClient;
import org.springframework.web.socket.messaging.WebSocketStompClient;
import org.springframework.web.socket.sockjs.client.SockJsClient;
import org.springframework.web.socket.sockjs.client.WebSocketTransport;

public class WebSocketServer {
    private static final String WEBSOCKET_URI = "ws://localhost:%s/websocket";
    private final WebSocketStompClient stompClient;
    private final int port;
    private final ObjectMapper objectMapper;
    private ConcurrentHashMap<UUID, StompSession> idToSession = new ConcurrentHashMap<>();
    private ConcurrentHashMap<UUID, BlockingQueue<String>> idToQueue = new ConcurrentHashMap<>();

    public WebSocketServer(int port) {
        this.stompClient = createStompClient();
        this.port = port;
        this.objectMapper = ObjectMapperConfig.create();
    }

    /**
     * Creates a new stomp session and stores connection for given client id.
     *
     * @param clientId User specified unique identifier for a client.
     * @throws Exception Throws error if a problem occurs connecting to stomp endpoint.
     */
    public void connect(UUID clientId) throws Exception {
        WebSocketHttpHeaders wsHeaders = new WebSocketHttpHeaders();
        StompHeaders connectHeaders = new StompHeaders();
        StompSession session = stompClient
            .connect(String.format(WEBSOCKET_URI, port), wsHeaders, connectHeaders,
                new StompSessionHandlerAdapter() {
                })
            .get(30, SECONDS);
        if (idToSession.containsKey(clientId)) {
            throw new SafaError("Attempting to override session");
        }
        idToSession.put(clientId, session);
        idToQueue.put(clientId, new LinkedBlockingDeque<>());
    }


    /**
     * Returns the next message in the queue associated with given client id.
     *
     * @param clientId The ID given to the client whose queue message is returned.
     * @return The next message in the queue.
     * @throws InterruptedException If interrupted while polling for message.
     */
    public String getMessage(UUID clientId, int timeToPoll) throws InterruptedException {
        return idToQueue.get(clientId).poll(timeToPoll, SECONDS);
    }

    /**
     * Returns all client messages.
     *
     * @param clientId   ID of client whose messages are retrieved.
     * @param timeToPoll The time to wait before retrieving messages.
     * @return List of messages.
     * @throws InterruptedException If interrupted during sleep.
     */
    public List<String> getMessages(UUID clientId, int timeToPoll) throws InterruptedException {
        Thread.sleep(timeToPoll);
        return new ArrayList<>(idToQueue.get(clientId));
    }

    /**
     * Sends message to destination.
     *
     * @param clientId    The client sending the message.
     * @param destination The destination of the message.
     * @param object      The payload to send.
     * @throws JsonProcessingException If error occurs while serializing object.
     */
    public void send(UUID clientId, String destination, Object object) throws JsonProcessingException {
        byte[] message = objectMapper.writeValueAsBytes(object);
        idToSession.get(clientId).send(destination, message);
    }

    /**
     * Clears the current sessions and queues.
     */
    public void clear() {
        this.idToSession.values().forEach(StompSession::disconnect);
        this.idToSession = new ConcurrentHashMap<>();
        this.idToQueue = new ConcurrentHashMap<>();
    }

    /**
     * Returns message queue for client.
     *
     * @param clientId The client whose queue is returned.
     */
    public BlockingQueue<String> getQueue(UUID clientId, int timeToPoll) throws InterruptedException {
        if (!this.idToQueue.containsKey(clientId)) {
            String error = String.format("%s does not have a queue. Has session been initialized?", clientId);
            throw new SafaError(error);
        }
        Thread.sleep(timeToPoll);
        return this.idToQueue.get(clientId);
    }

    /**
     * Clears the current messages for given client.
     *
     * @param clientId ID of client to clear messages for.
     */
    public void clearQueue(UUID clientId) {
        this.idToQueue.get(clientId).clear();
    }

    /**
     * Subscribe clientId to destination, storing messages from a topic in the queue.
     *
     * @param clientId    The client subscribing to messages.
     * @param destination The destionation to subscribe to.
     */
    public void subscribe(UUID clientId, String destination) {
        idToSession.get(clientId).subscribe(destination, new StompFrameHandler() {
            @NotNull
            public Type getPayloadType(@NotNull StompHeaders stompHeaders) {
                return byte[].class;
            }

            public void handleFrame(@NotNull StompHeaders stompHeaders, Object o) {
                idToQueue.get(clientId).offer(new String((byte[]) o));
            }
        });
    }

    private WebSocketStompClient createStompClient() {
        StandardWebSocketClient webSocketClient = new StandardWebSocketClient();
        WebSocketTransport transport = new WebSocketTransport(webSocketClient);
        SockJsClient client = new SockJsClient(List.of(transport));
        WebSocketStompClient stompClient = new WebSocketStompClient(client);
        stompClient.setInboundMessageSizeLimit(WebSocketBrokerConfig.MESSAGE_SIZE_LIMIT);
        return stompClient;
    }
}
