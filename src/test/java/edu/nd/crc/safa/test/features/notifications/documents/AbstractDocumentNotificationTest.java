package edu.nd.crc.safa.test.features.notifications.documents;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.documents.entities.app.DocumentColumnAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.test.features.notifications.AbstractNotificationTest;

import org.json.JSONObject;

public abstract class AbstractDocumentNotificationTest extends AbstractNotificationTest {
    /**
     * ID of document being manipulated.
     */
    protected UUID documentId;
    /**
     * Instance of constants, including document being manipulated
     */
    protected DocumentConstants documentConstants = new DocumentConstants();

    protected void createDocumentAndVerifyMessage() throws Exception {
        this.createDocument();
        EntityChangeMessage message = this.notificationService.getNextMessage(Sharee.email);
        this.changeMessageVerifies.verifyDocumentChange(
            message,
            this.documentId,
            Change.Action.UPDATE
        );
        this.changeMessageVerifies.verifyUpdateLayout(message, false);
    }

    protected void createDocument() throws Exception {
        DocumentAppEntity documentAppEntity = this.documentConstants.document;
        JSONObject response = this.creationService.createOrUpdateDocument(
            this.projectVersion,
            documentAppEntity);
        this.documentId = documentAppEntity.getDocumentId();
    }

    public static class DocumentConstants {
        private final String name = "document-name";
        private final String description = "document-description";
        private final List<UUID> artifactIds = new ArrayList<>();
        private final List<DocumentColumnAppEntity> columns = new ArrayList();
        public final DocumentAppEntity document = new DocumentAppEntity(
            null,
            DocumentType.ARTIFACT_TREE,
            name,
            description,
            artifactIds,
            columns,
            new HashMap<>()
        );
    }
}
