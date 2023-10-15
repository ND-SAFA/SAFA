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
import edu.nd.crc.safa.config.SecurityConstants;
import edu.nd.crc.safa.config.WebSocketBrokerConfig;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.jetbrains.annotations.NotNull;
import org.springframework.lang.Nullable;
import org.springframework.messaging.simp.stomp.StompCommand;
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
    private static WebSocketStompClient client;
    private final int port;
    private final ObjectMapper objectMapper;
    private ConcurrentHashMap<UUID, StompSession> idToSession = new ConcurrentHashMap<>();
    private ConcurrentHashMap<UUID, BlockingQueue<String>> idToQueue = new ConcurrentHashMap<>();

    public WebSocketServer(int port) {
        this.port = port;
        this.objectMapper = ObjectMapperConfig.create();
    }

    private static WebSocketStompClient getStompClient() {
        if (WebSocketServer.client == null) {
            StandardWebSocketClient webSocketClient = new StandardWebSocketClient();
            WebSocketTransport transport = new WebSocketTransport(webSocketClient);
            SockJsClient client = new SockJsClient(List.of(transport));
            WebSocketStompClient stompClient = new WebSocketStompClient(client);
            stompClient.setInboundMessageSizeLimit(WebSocketBrokerConfig.MESSAGE_SIZE_LIMIT);
            WebSocketServer.client = stompClient;
        }
        return WebSocketServer.client;
    }

    /**
     * Creates a new stomp session and stores connection for given client id.
     *
     * @param clientId User specified unique identifier for a client.
     * @throws Exception Throws error if a problem occurs connecting to stomp endpoint.
     */
    public void connect(UUID clientId, String token) throws Exception {
        String cookieValue = String.format("%s=%s", SecurityConstants.JWT_COOKIE_NAME, token);

        WebSocketHttpHeaders connectionHeaders = new WebSocketHttpHeaders();
        connectionHeaders.put(SecurityConstants.COOKIE_NAME, List.of(cookieValue));

        StompHeaders messageHeaders = new StompHeaders();

        StompSession session = getStompClient()
            .connect(String.format(WEBSOCKET_URI, port), connectionHeaders, messageHeaders,
                new StompSessionHandlerAdapter() {
                    @Override
                    public void handleException(StompSession session, @Nullable StompCommand command,
                                                StompHeaders headers, byte[] payload, Throwable exception) {
                        exception.printStackTrace();
                    }
                })
            .get(30, SECONDS);
        if (idToSession.containsKey(clientId)) {
            String error = String.format("Attempting to override session, Client %s has session.", clientId);
            throw new SafaError(error);
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
        assertClientExists(clientId);
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
    public List<String> getMessages(UUID clientId, int timeToPoll) {
        try {
            assertClientExists(clientId);
            Thread.sleep(timeToPoll);
            return new ArrayList<>(idToQueue.get(clientId));
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
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
        assertClientExists(clientId);
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
        assertClientExists(clientId);
        Thread.sleep(timeToPoll);
        return this.idToQueue.get(clientId);
    }

    /**
     * Clears the current messages for given client.
     *
     * @param clientId ID of client to clear messages for.
     */
    public void clearQueue(UUID clientId) {
        assertClientExists(clientId);
        this.idToQueue.get(clientId).clear();
    }

    /**
     * Subscribe clientId to destination, storing messages from a topic in the queue.
     *
     * @param clientId    Unique identifier for user.
     * @param destination The destination to subscribe to.
     */
    public void subscribe(UUID clientId, String destination) {
        assertClientExists(clientId);
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

    private void assertClientExists(UUID clientId) {
        String errorMessage = "%s does not have a %s. Has session been initialized?";
        if (!this.idToQueue.containsKey(clientId)) {
            throw new SafaError(String.format(errorMessage, clientId, "queue"));
        }
        if (!this.idToSession.containsKey(clientId)) {
            throw new SafaError(String.format(errorMessage, clientId, "session"));
        }
    }
}
