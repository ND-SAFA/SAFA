package edu.nd.crc.safa.test.common;

import java.io.IOException;

import lombok.Getter;
import okhttp3.mockwebserver.MockWebServer;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;

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

    @AfterAll
    public static void teardownWebServer() throws IOException {
        mockWebServer.shutdown();
    }
}
