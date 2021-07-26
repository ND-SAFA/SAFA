package edu.nd.crc.safa.routes;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONObject;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;

public class ErrorTest extends MvcBaseTest {

    @Test
    public void testUploadError() throws Exception {
        String projectID = "abc123";
        String URL = String.format("/projects/%s/upload/", projectID);
        MockHttpServletRequestBuilder request = post(URL)
            .contentType(MediaType.APPLICATION_JSON)
            .content(asJsonString("hello world"));
        MvcResult result = mockMvc
            .perform(request)
            .andExpect(status().isBadRequest())
            .andReturn();

        String content = result.getResponse().getContentAsString();
        JSONObject obj = new JSONObject(content);
        Assert.assertEquals(obj.get("status"), 1);
        Assert.assertTrue(obj.getJSONObject("body").get("message").toString().contains("parsing json file"));
    }

    public static String asJsonString(final Object obj) {
        try {
            return new ObjectMapper().writeValueAsString(obj);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
