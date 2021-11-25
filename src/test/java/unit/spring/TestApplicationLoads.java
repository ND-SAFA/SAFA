package unit.spring;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import unit.SpringBootBaseTest;

/**
 * Tests that SpringBoot application is loaded and dependency injection
 * can be performed.
 */
public class TestApplicationLoads extends SpringBootBaseTest {

    @Test
    public void contextLoads() {
        assertThat(controller).isNotNull();
    }
}
