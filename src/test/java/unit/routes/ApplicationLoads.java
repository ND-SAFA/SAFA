package unit.routes;

import static org.assertj.core.api.Assertions.assertThat;
import static org.hamcrest.Matchers.containsString;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.importer.MySQL;

import org.junit.jupiter.api.Test;
import unit.SpringBootBaseTest;

/**
 * Tests that SpringBoot application is loaded and dependency injection
 * can be performed.
 */
public class ApplicationLoads extends SpringBootBaseTest {

    @Test
    public void contextLoads() throws Exception {
        assertThat(controller).isNotNull();
    }

    @Test
    public void testHelloWorld() throws Exception {
        this.mockMvc.perform(get("/")).andExpect(status().isOk())
            .andExpect(content().string(containsString("Hello World")));
    }

    @Test
    public void testSQLConnection() throws Exception {
        MySQL sql = new MySQL();
        sql.verifyConnection();
    }
}
