package unit.routes;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.importer.MySQL;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MvcResult;
import unit.SpringBootBaseTest;
import unit.TestUtil;

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
        MvcResult result = this.mockMvc.perform(get("/")).andExpect(status().isOk()).andReturn();
        JSONObject content = TestUtil.asJson(result);
        assertThat(content.get("status")).isEqualTo(0);
        assertThat(content.get("body")).isEqualTo("Hello World");
    }

    @Test
    public void testSQLConnection() throws Exception {
        MySQL sql = new MySQL();
        sql.verifyConnection();
    }
}
