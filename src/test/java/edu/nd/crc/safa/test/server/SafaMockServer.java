package edu.nd.crc.safa.test.server;

import java.io.IOException;
import java.util.Queue;

import edu.nd.crc.safa.config.ObjectMapperConfig;

import com.google.errorprone.annotations.ForOverride;
import lombok.Getter;
import okhttp3.mockwebserver.MockResponse;
import okhttp3.mockwebserver.MockWebServer;
import okhttp3.mockwebserver.QueueDispatcher;
import okhttp3.mockwebserver.RecordedRequest;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.test.util.ReflectionTestUtils;

public class SafaMockServer {
    private boolean isRunning = false;
    @Getter
    private MockWebServer mockWebServer;
    @Getter
    private String remoteApiUrl;

    /**
     * Starts the web server on a random port.
     */
    public void start() {
        if (isRunning)
            return;
        try {
            mockWebServer = new MockWebServer();
            mockWebServer.start();
            remoteApiUrl = String.format("http://localhost:%s", mockWebServer.getPort());
            isRunning = true;
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        afterInit();
    }

    /**
     * Safely stops the server.
     *
     * @throws IOException If error occurs while shutting down.
     */
    public void stop() throws IOException {
        if (isRunning) {
            mockWebServer.shutdown();
        }
    }

    /**
     * Sets the next response to be the JSON representation object.
     *
     * @param object The object to return in request.
     */
    public void setResponse(Object object) {
        start();
        try {
            String objectString = ObjectMapperConfig.create().writeValueAsString(object);
            MockResponse response = new MockResponse()
                .setBody(objectString)
                .addHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE);
            mockWebServer.enqueue(response);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * Adds JSON string as response in server queue.
     *
     * @param json The response to request.
     */
    public void setStringResponse(String json) {
        mockWebServer.enqueue(new MockResponse()
            .setBody(json)
            .addHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE));
    }

    /**
     * Clears the current server queue of responses.
     */
    public void clear() {
        QueueDispatcher dispatcher = (QueueDispatcher) mockWebServer.getDispatcher();
        Queue<MockResponse> responseQueue = (Queue<MockResponse>) ReflectionTestUtils.getField(dispatcher, "responseQueue");
        assert responseQueue != null;
        responseQueue.clear();
    }

    /**
     * Returns request next in queue to server.
     *
     * @return HTTP request to mock server.
     * @throws InterruptedException
     */
    public RecordedRequest takeRequest() throws InterruptedException {
        return getMockWebServer().takeRequest();
    }

    /**
     * Peeks the next response in mock server.
     *
     * @return The server response.
     */
    public MockResponse peekResponse() {
        return getMockWebServer().getDispatcher().peek();
    }

    /**
     * Handler for performing operations after server is initialized.
     */
    @ForOverride
    protected void afterInit() {
    }

}
