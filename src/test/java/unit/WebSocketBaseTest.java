package unit;

import static java.util.concurrent.TimeUnit.SECONDS;

import java.lang.reflect.Type;
import java.util.HashMap;
import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingDeque;

import edu.nd.crc.safa.config.WebSocketBrokerConfig;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.messaging.simp.stomp.StompFrameHandler;
import org.springframework.messaging.simp.stomp.StompHeaders;
import org.springframework.messaging.simp.stomp.StompSession;
import org.springframework.messaging.simp.stomp.StompSessionHandlerAdapter;
import org.springframework.web.socket.WebSocketHttpHeaders;
import org.springframework.web.socket.client.standard.StandardWebSocketClient;
import org.springframework.web.socket.messaging.WebSocketStompClient;
import org.springframework.web.socket.sockjs.client.SockJsClient;
import org.springframework.web.socket.sockjs.client.WebSocketTransport;

/**
 * Provides an abstraction over the websocket connection enabling:
 * 1. connecting to server through websocket endpoint
 * 2. Reading messages in queue associated
 */
public class WebSocketBaseTest extends ApplicationBaseTest {

    static final String WEBSOCKET_URI = "ws://localhost:%s/websocket";
    private static ObjectMapper mapper;
    private static WebSocketStompClient stompClient;
    private static HashMap<String, BlockingQueue<String>> idToQueue;
    private static HashMap<String, StompSession> idToSession;

    final int TIME_TO_POLL_SECONDS = 5; // seconds
    final int TIME_TO_POLL_MS = TIME_TO_POLL_SECONDS * 1000;

    @LocalServerPort
    private Integer port;

    @BeforeAll
    public static void setup() {
        mapper = new ObjectMapper();
        idToQueue = new HashMap<>();
        idToSession = new HashMap<>();
        StandardWebSocketClient webSocketClient = new StandardWebSocketClient();
        WebSocketTransport transport = new WebSocketTransport(webSocketClient);
        SockJsClient client = new SockJsClient(List.of(transport));
        stompClient = new WebSocketStompClient(client);
        stompClient.setInboundMessageSizeLimit(WebSocketBrokerConfig.messageSizeLimit);
    }

    @BeforeEach
    public void clearQueue() {
        idToQueue = new HashMap<>();
    }

    public WebSocketBaseTest createNewConnection(String id) throws Exception {
        assertTokenExists();
        WebSocketHttpHeaders headers = new WebSocketHttpHeaders();
        StompSession session = stompClient
            .connect(String.format(WEBSOCKET_URI, port),
                new StompSessionHandlerAdapter() {
                })
            .get(1, SECONDS);
        idToSession.put(id, session);
        idToQueue.put(id, new LinkedBlockingDeque<>());
        return this;
    }

    public WebSocketBaseTest subscribe(String id, String topic) {
        idToSession.get(id).subscribe(topic, new StompFrameHandler() {
            public Type getPayloadType(StompHeaders stompHeaders) {
                return byte[].class;
            }

            public void handleFrame(StompHeaders stompHeaders, Object o) {
                idToQueue.get(id).offer(new String((byte[]) o));
            }
        });
        return this;
    }

    public <T> T getNextMessage(String id, Class<T> tClass) throws InterruptedException, JsonProcessingException {
        String response = getNextMessage(id);
        return mapper.readValue(response, tClass);
    }

    public String getNextMessage(String id) throws InterruptedException {
        return idToQueue.get(id).poll(TIME_TO_POLL_SECONDS, SECONDS);
    }

    public int getQueueSize(String id) throws InterruptedException {
        Thread.sleep(500);
        return idToQueue.get(id).size();
    }
}
