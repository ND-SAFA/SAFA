package edu.nd.crc.safa.routes;

import edu.nd.crc.safa.controller.projects.ProjectsController;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
public abstract class MvcBaseTest {

    @Autowired
    protected MockMvc mockMvc;

    @Autowired
    protected ProjectsController controller;
}
