package edu.nd.crc.safa.controller;

import edu.nd.crc.safa.controller.projects.ProjectsController;

import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.context.web.WebAppConfiguration;

@RunWith(SpringRunner.class)
@SpringBootTest
@WebAppConfiguration
@AutoConfigureMockMvc
public class API {

    @Autowired
    private ProjectsController controller;

    @Test
    public void contextLoads() {
        assert controller != null;
    }
}
