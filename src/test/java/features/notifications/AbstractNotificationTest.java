package features.notifications;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;

import common.AbstractSharingTest;
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
     * @param message Message as a result of performing action.
     */
    protected abstract void verifyShareeMessage(EntityChangeMessage message);

    @Test
    public void notificationTest() throws Exception {
        // Step - Perform action with default user
        performAction();

        // VP - Verify that single message sent
        assertThat(notificationTestService.getQueueSize(Sharee.email))
            .as("single message for flat file upload")
            .isEqualTo(1);

        // Step - Retrieve action message
        EntityChangeMessage actionMessage = this.notificationTestService.getNextMessage(Sharee.email);

        // VP - Verify message correctness
        verifyShareeMessage(actionMessage);
    }
}
