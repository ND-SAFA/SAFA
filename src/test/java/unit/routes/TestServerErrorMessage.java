package unit.routes;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.UUID;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MvcResult;
import unit.SpringBootBaseTest;
import unit.TestUtil;

/**
 * Tests that server errors include a
 * - status (0 if success otherwise some error code > 0)
 * - body (contains error message and other information)
 */
public class TestServerErrorMessage extends SpringBootBaseTest {

    @Test
    public void testServerError() throws Exception {
        String projectId = UUID.randomUUID().toString(); // not exist
        String routeName = String.format("/projects/versions/%s", projectId);

        MvcResult result = mockMvc
            .perform(get(routeName))
            .andExpect(status().isBadRequest())
            .andReturn();

        JSONObject obj = TestUtil.asJson(result);

        //Verification Points
        Integer responseStatus = (Integer) obj.get("status");

        assertThat(responseStatus).isNotNull();
        assertThat(responseStatus).isEqualTo(1);

        JSONObject body = obj.getJSONObject("body");
        assertThat(body).isNotNull();

        Object error = body.get("message");
        assertThat(error).isNotNull();
    }
}
