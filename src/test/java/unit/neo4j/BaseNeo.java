package unit.neo4j;

import edu.nd.crc.safa.repositories.neo4j.ArtifactNodeRepository;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.neo4j.harness.Neo4j;
import org.neo4j.harness.Neo4jBuilders;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import unit.SpringBootBaseTest;

public class BaseNeo extends SpringBootBaseTest {

    protected static Neo4j embeddedDatabaseServer;

    static {
        org.neo4j.internal.unsafe.IllegalAccessLoggerSuppressor.suppress();
    }

    @Autowired
    protected ArtifactNodeRepository artifactNodeRepository;

    @BeforeAll
    static void startServer() {
        if (embeddedDatabaseServer == null) {
            embeddedDatabaseServer = Neo4jBuilders
                .newInProcessBuilder()
                .withDisabledServer()
                .build();
        }
    }

    @DynamicPropertySource
    static void neo4jProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.neo4j.uri", embeddedDatabaseServer::boltURI);
        registry.add("spring.neo4j.authentication.username", () -> "neo4j");
        registry.add("spring.neo4j.authentication.password", () -> null);
    }

    @AfterAll
    static void stopServer() {
        if (embeddedDatabaseServer != null) {
            embeddedDatabaseServer.close();
            System.out.println("Closing server");
        }
    }
}
