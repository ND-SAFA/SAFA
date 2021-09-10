package unit.controllers;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.UUID;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.EntityBaseTest;

/**
 * Tests that server errors include a
 * - status (0 if success otherwise some error code > 0)
 * - body (contains error message and other information)
 */
public class TestServerErrorMessage extends EntityBaseTest {

    @Test
    public void testServerError() throws Exception {
        String projectId = UUID.randomUUID().toString(); // not exist
        String routeName = String.format("/projects/%s/versions", projectId);

        JSONObject obj = sendGet(routeName, status().isBadRequest());

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
