package unit;

import javax.annotation.PostConstruct;
import javax.persistence.EntityManager;

import edu.nd.crc.safa.MainApplication;
import edu.nd.crc.safa.server.controllers.ProjectController;
import edu.nd.crc.safa.server.services.ServiceProvider;

import org.springframework.batch.core.launch.support.SimpleJobLauncher;
import org.springframework.batch.core.repository.JobRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.core.task.SyncTaskExecutor;
import org.springframework.test.web.servlet.MockMvc;

/**
 * Responsible for providing access to application classes
 * using SpringBoot's test loader annotations.
 */
@SpringBootTest(classes = MainApplication.class, webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureMockMvc
public abstract class SpringBootBaseTest {

    @Autowired
    protected MockMvc mockMvc;

    @Autowired
    protected ProjectController controller;

    @Autowired
    protected EntityManager entityManager;

    @Autowired
    protected ServiceProvider serviceProvider;

    @Autowired
    JobRepository jobRepository;

    /**
     * Sets the current job launcher to run job synchronously so that
     *
     * @throws Exception Throws exception is error encountered during afterPropertiesSet.
     */
    @PostConstruct
    public void afterConstruct() throws Exception {
        SimpleJobLauncher jobLauncher = new SimpleJobLauncher();
        jobLauncher.setJobRepository(jobRepository);
        jobLauncher.setTaskExecutor(new SyncTaskExecutor());
        jobLauncher.afterPropertiesSet();

        serviceProvider.setJobLauncher(jobLauncher);
    }
}
