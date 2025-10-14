package edu.nd.crc.safa.test.common;

import java.io.IOException;

import edu.nd.crc.safa.test.server.SafaMockServer;

import lombok.Getter;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.TestInstance;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public abstract class AbstractRemoteApiTest<T extends SafaMockServer> extends ApplicationBaseTest {
    @Getter
    private T server;

    /**
     * Creates the common server and starts it.
     */
    @BeforeAll
    public void initSuite() {
        server = createServer();
        server.start();
    }

    /**
     * Clears the response queue before each test.
     */
    @BeforeEach
    public void clearWebServerQueue() {
        server.clear();
    }

    /**
     * Stops server after all tests have finished.
     *
     * @throws IOException If error occurs during shutdown.
     */
    @AfterAll
    public void teardownWebServer() throws IOException {
        server.stop();
    }

    /**
     * @return Returns the path to server URL.
     */
    public String getRemoteApiUrl() {
        return server.getRemoteApiUrl();
    }

    /**
     * Creates server instance. Used to override with different types of servers.
     *
     * @return The server to use in test.
     */
    public T createServer() {
        return (T) new SafaMockServer();
    }
}
