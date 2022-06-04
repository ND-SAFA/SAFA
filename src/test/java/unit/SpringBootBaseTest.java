package unit;

import javax.persistence.EntityManager;

import edu.nd.crc.safa.MainApplication;
import edu.nd.crc.safa.config.TestConfig;
import edu.nd.crc.safa.server.controllers.ProjectController;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.web.servlet.MockMvc;

/**
 * Responsible for providing access to application classes
 * using SpringBoot's test loader annotations.
 */
@SpringBootTest(classes = MainApplication.class, webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureMockMvc
@Import(TestConfig.class)
public abstract class SpringBootBaseTest {

    @Autowired
    protected MockMvc mockMvc;

    @Autowired
    protected ProjectController controller;

    @Autowired
    protected EntityManager entityManager;
}
