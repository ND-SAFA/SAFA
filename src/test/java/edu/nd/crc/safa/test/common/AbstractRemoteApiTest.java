package edu.nd.crc.safa.test.common;

import java.io.IOException;
import java.util.Queue;

import lombok.Getter;
import okhttp3.mockwebserver.MockResponse;
import okhttp3.mockwebserver.MockWebServer;
import okhttp3.mockwebserver.QueueDispatcher;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.test.util.ReflectionTestUtils;

public abstract class AbstractRemoteApiTest extends ApplicationBaseTest {
    @Getter
    private static MockWebServer mockWebServer;

    @Getter
    private static String remoteApiUrl;

    @BeforeAll
    public static void setupWebServer() throws IOException {
        mockWebServer = new MockWebServer();
        mockWebServer.start();

        remoteApiUrl = String.format("http://localhost:%s", mockWebServer.getPort());
    }

    @BeforeEach
    public void clearWebServerQueue() {
        QueueDispatcher dispatcher = (QueueDispatcher) mockWebServer.getDispatcher();
        Queue<MockResponse> responseQueue = (Queue<MockResponse>) ReflectionTestUtils.getField(dispatcher, "responseQueue");
        assert responseQueue != null;
        responseQueue.clear();
    }

    @AfterAll
    public static void teardownWebServer() throws IOException {
        mockWebServer.shutdown();
    }
}
