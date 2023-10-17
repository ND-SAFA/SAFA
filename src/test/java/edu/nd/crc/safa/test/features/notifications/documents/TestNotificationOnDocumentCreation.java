package edu.nd.crc.safa.test.features.notifications.documents;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;

import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;

/**
 * Test that creating a document sends notification containing:
 * - single change
 * - change entity is DOCUMENT
 * - change action is UPDATE
 * - change contains Document.id
 */
public class TestNotificationOnDocumentCreation extends AbstractDocumentNotificationTest {

    @Override
    protected void performAction() throws Exception {
        this.createDocument();
    }

    @Override
    protected void verifyShareeMessages(List<EntityChangeMessage> messages) {
        assertEquals(1, messages.size());
        EntityChangeMessage message = messages.get(0);
        this.messageVerificationService.verifyDocumentChange(
            message,
            this.documentId,
            NotificationAction.UPDATE
        );
        this.messageVerificationService.verifyUpdateLayout(message, false);
    }
}
