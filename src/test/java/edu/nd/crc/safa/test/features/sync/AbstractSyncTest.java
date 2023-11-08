package edu.nd.crc.safa.test.features.sync;

import java.util.List;

import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;

/**
 * Test that correct entities are retrived for an EntityChangeMessage
 */
public abstract class AbstractSyncTest extends ApplicationBaseTest {

    /**
     * Converts JSON response to {@link ProjectAppEntity}
     */
    private final ObjectMapper objectMapper = ObjectMapperConfig.create();
    /**
     * Project created.
     */
    protected ProjectVersion projectVersion;

    public AbstractSyncTest() {
        objectMapper.findAndRegisterModules();
    }

    @Test
    public void runTest() throws Exception {

        // Step - Create project and version
        this.projectVersion = this.creationService.createProjectWithNewVersion(projectName);

        // Step - Subscribe user to version
        this.rootBuilder
            .notifications(n -> n
                .initializeUser(getCurrentUser(), getToken(getCurrentUser()))
                .subscribeToVersion(getCurrentUser(), projectVersion));

        // Step - Perform action on project
        this.performAction();

        // VP - Verify correctness of message
        List<EntityChangeMessage> actionMessage = this.rootBuilder.notifications(n -> n.getMessages(getCurrentUser())).get();
        this.verifyActionMessage(actionMessage);
    }

    abstract void performAction() throws Exception;

    /**
     * Verifies that message is correct as a result of action.
     *
     * @param messages The notification sent after action
     */
    abstract void verifyActionMessage(List<EntityChangeMessage> messages);
}
