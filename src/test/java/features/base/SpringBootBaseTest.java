package features.base;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import javax.annotation.PostConstruct;
import javax.sql.DataSource;

import edu.nd.crc.safa.MainApplication;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.projects.controllers.ProjectController;

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
    protected ServiceProvider serviceProvider;

    @Autowired
    JobRepository jobRepository;

    @Autowired
    DataSource dataSource;

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

    /**
     * Sets the testing database's mode, H2, to legacy in order for spring
     * batch to be able to initialize its own tables.
     *
     * @throws SQLException Throws exception if unable to set legacy mode.
     */
    @PostConstruct
    public void setLegacyModeInH2Database() throws SQLException {
        String query = "SET MODE LEGACY;\n";
        Connection connection = this.dataSource.getConnection();
        try (Statement statement = connection.createStatement()) {
            statement.execute(query);
        }
        connection.close();
    }
}
