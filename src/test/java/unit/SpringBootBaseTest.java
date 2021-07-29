package unit;

import edu.nd.crc.safa.MainApplication;
import edu.nd.crc.safa.controllers.OldController;

import org.hibernate.SessionFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

/**
 * Responsible for providing access to application classes
 * using SpringBoot's test loader annotations.
 */
@SpringBootTest(classes = MainApplication.class)
@AutoConfigureMockMvc
public abstract class SpringBootBaseTest {

    @Autowired
    protected MockMvc mockMvc;

    @Autowired
    protected OldController controller;

    @Autowired
    public SessionFactory sessionFactory;
}
