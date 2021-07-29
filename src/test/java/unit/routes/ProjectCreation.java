package unit.routes;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;

import org.junit.jupiter.api.Test;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.SpringBootBaseTest;

public class ProjectCreation extends SpringBootBaseTest {
    @Test
    public void testMultipleFilesUploadRestController() throws Exception {
        mockMvc.perform(post("/projects/flat-files")
            .contentType(MediaType.APPLICATION_JSON)
            .content("")).andExpect(MockMvcResultMatchers.status().isNoContent());
    }
}
