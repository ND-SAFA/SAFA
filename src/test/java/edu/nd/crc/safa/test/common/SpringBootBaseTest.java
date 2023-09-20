package edu.nd.crc.safa.test.common;

import javax.sql.DataSource;

import edu.nd.crc.safa.MainApplication;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.projects.controllers.ProjectController;

import org.springframework.batch.core.repository.JobRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.web.servlet.MockMvc;

/**
 * Responsible for providing access to application classes
 * using SpringBoot's test loader annotations.
 */
@SpringBootTest(classes = MainApplication.class, webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureMockMvc
@ContextConfiguration(classes = MainApplication.class)
public abstract class SpringBootBaseTest {

    @Autowired
    protected MockMvc mockMvc;

    @Autowired
    protected ProjectController controller;

    @Autowired
    protected ServiceProvider serviceProvider;

    @Autowired
    JobRepository jobRepository;

    @Autowired
    DataSource dataSource;
}
