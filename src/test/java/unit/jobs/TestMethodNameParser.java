package unit.jobs;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import edu.nd.crc.safa.server.services.JobService;
import edu.nd.crc.safa.utilities.MethodNameParser;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

/**
 * Responsible for testing that the step numbers for
 * Job workers are being parsed correctly.
 */
public class TestMethodNameParser extends ApplicationBaseTest {
    @Autowired
    JobService jobService;

    @Test
    public void parseProjectCreationSteps() {
        int numberOfSteps = 12;
        String prefix = "step";

        for (int i = 0; i < numberOfSteps; i++) {
            String stepName = prefix + i + "Create";
            int result = MethodNameParser.getNumberAfterPrefix(stepName, prefix);
            assertThat(result).isEqualTo(i);
        }
    }

    @Test
    public void expectError() {
        assertThrows(RuntimeException.class, () -> {
            MethodNameParser.getNumberAfterPrefix("stepOneCreate", "step");
        });
    }
}
