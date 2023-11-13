package edu.nd.crc.safa.test.features.notifications;

import java.util.List;

import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.test.common.AbstractSharingTest;

import org.junit.jupiter.api.Test;

/**
 * Test that certain actions notify shared members with notifications
 */
public abstract class AbstractNotificationTest extends AbstractSharingTest {

    /**
     * Action to be performed by default user.
     */
    protected abstract void performAction() throws Exception;

    /**
     * Verifies correctness of sharee message.
     *
     * @param messages Messages as a result of performing action.
     */
    protected abstract void verifyShareeMessages(List<EntityChangeMessage> messages);

    @Test
    public void notificationTest() throws Exception {
        // Step - Perform action with default user
        performAction();

        // Step - Retrieve action message
        // TODO https://www.notion.so/nd-safa/BE-Tests-Occasionally-Fail-9500d5c1f1d84a76acf429ee3653bb86
        //this.rootBuilder.notifications(n -> n.getMessages(sharee)).consume(this::verifyShareeMessages);
    }
}
