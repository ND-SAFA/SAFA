package unit.routes;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;

import java.util.List;

import edu.nd.crc.safa.constants.ProjectPaths;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.SpringBootBaseTest;
import unit.TestUtil;
import unit.utilities.TestFileUtility;

public class TestProjectCreation extends SpringBootBaseTest {


    @Test
    @Disabled
    public void testMultipleFilesUploadRestController() throws Exception {

        String attributeName = "files";
        String routeName = "/projects/flat-files";

        List<MockMultipartFile> files =
            TestFileUtility.createMockMultipartFilesFromDirectory(ProjectPaths.PATH_TO_TEST_RESOURCES,
                attributeName);
        MockMultipartHttpServletRequestBuilder request = multipart(routeName);

        for (MockMultipartFile file : files) {
            request.file(file);
        }


        MvcResult response = mockMvc
            .perform(request)
            .andExpect(MockMvcResultMatchers.status().isNoContent())
            .andReturn();

        //Verification Points
        assertThat(response).isNotNull();
        System.out.println("response:" + response);
        JSONObject responseContent = TestUtil.asJson(response);
        assertThat(responseContent.get("status")).isEqualTo(0);
        JSONObject responseBody = responseContent.getJSONObject("body");
        assertThat(responseBody).isNotNull();
        JSONArray filesReceived = responseBody.getJSONArray("filesReceived");
        assertThat(filesReceived).isNotNull();
        assertThat(filesReceived.length()).isEqualTo(1);
        assertThat(filesReceived.get(0)).isEqualTo("tim.json");
    }
}
