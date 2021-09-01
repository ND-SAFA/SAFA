package unit.neo4j;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;

public class TestConnection extends BaseNeo {
    @Test
    public void testServerStarted() {
        assertThat(embeddedDatabaseServer).isNotNull();
    }
}
