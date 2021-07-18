package edu.nd.crc.safa.controller;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;

import edu.nd.crc.safa.controller.projects.ProjectsController;

import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.test.web.servlet.MockMvc;

@RunWith(SpringRunner.class)
@SpringBootTest
@WebAppConfiguration
@AutoConfigureMockMvc
public class API {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ProjectsController controller;

    @Test
    public void contextLoads() {
        assert controller != null;
    }

    @Test
    public void testConnections() throws Exception {
        mockMvc.perform(get("/connections"));
    }
}
