package unit.routes;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;

import java.io.File;

import edu.nd.crc.safa.constants.ProjectPaths;

import org.apache.commons.io.FileUtils;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.RequestBuilder;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.SpringBootBaseTest;
import unit.TestUtil;

public class ProjectCreation extends SpringBootBaseTest {
    @Test
    public void testMultipleFilesUploadRestController() throws Exception {
        String fileName = "tim.json";
        String pathToFile = ProjectPaths.PATH_TO_TEST_RESOURCES + "/" + fileName;
        File timFile = new File(pathToFile);
        assertThat(timFile.exists()).isTrue();

        byte[] fileContent = FileUtils.readFileToByteArray(timFile);
        MockMultipartFile requestTimeFile = new MockMultipartFile(
            "files",
            fileName,
            "application/json",
            fileContent);
        RequestBuilder request = multipart("/projects/flat-files")
            .file(requestTimeFile);
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
