package unit.routes;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;
import unit.SpringBootBaseTest;
import unit.TestUtil;

/**
 * Tests that server errors include a
 * - status (0 if success otherwise some error code > 0)
 * - body (contains error message and other information)
 */
public class ServerErrorMessage extends SpringBootBaseTest {

    @Test
    public void testServerError() throws Exception {
        String projectID = "abc123";
        String URL = String.format("/projects/%s/upload/", projectID);
        MockHttpServletRequestBuilder request = post(URL)
            .contentType(MediaType.APPLICATION_JSON)
            .content(TestUtil.asJsonString("hello world"));
        MvcResult result = mockMvc
            .perform(request)
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
