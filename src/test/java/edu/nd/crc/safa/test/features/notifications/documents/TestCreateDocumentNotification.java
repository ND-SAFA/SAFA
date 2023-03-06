package edu.nd.crc.safa.test.features.notifications.documents;

import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;

/**
 * Test that creating a document sends notification containing:
 * - single change
 * - change entity is DOCUMENT
 * - change action is UPDATE
 * - change contains Document.id
 */
public class TestCreateDocumentNotification extends AbstractDocumentNotificationTest {

    @Override
    protected void performAction() throws Exception {
        this.createDocument();
    }

    @Override
    protected void verifyShareeMessage(EntityChangeMessage message) {
        this.changeMessageVerifies.verifyDocumentChange(
            message,
            this.documentId,
            Change.Action.UPDATE
        );
        this.changeMessageVerifies.verifyUpdateLayout(message, false);
    }
}
