package features.notifications.documents;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.documents.entities.app.DocumentColumnAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;

import features.notifications.AbstractNotificationTest;
import org.json.JSONObject;
import requests.SafaRequest;

public abstract class AbstractDocumentNotificationTest extends AbstractNotificationTest {
    /**
     * ID of document being manipulated.
     */
    protected UUID documentId;
    /**
     * Instance of constants, including document being manipulated
     */
    Constants constants = new Constants();

    protected void createDocument() throws Exception {
        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Documents.CREATE_OR_UPDATE_DOCUMENT)
            .withVersion(projectVersion)
            .postWithJsonObject(constants.document);
        this.documentId = UUID.fromString(response.getString("documentId"));
        this.constants.document.setDocumentId(this.documentId.toString());
    }

    @Override
    protected void verifyShareeMessage(EntityChangeMessage message) {
        this.verifyDocumentMessage(message, Change.Action.UPDATE);
    }

    protected void verifyDocumentMessage(EntityChangeMessage message,
                                         Change.Action action) {
        assertThat(message.getChanges())
            .as("single change in message")
            .hasSize(1);

        Change change = message.getChanges().get(0);

        assertThat(change.getEntity())
            .as("Entity = DOCUMENT")
            .isEqualTo(Change.Entity.DOCUMENT);
        assertThat(change.getAction())
            .as("Action = UPDATE")
            .isEqualTo(action);
        assertThat(change.getEntityIds())
            .as("Entity ID = Document.id")
            .hasSize(1).contains(this.documentId);
    }

    static class Constants {
        private final String name = "document-name";
        private final String description = "document-description";
        private final List<String> artifactIds = new ArrayList<>();
        private final List<DocumentColumnAppEntity> columns = new ArrayList();
        final DocumentAppEntity document = new DocumentAppEntity(
            "",
            DocumentType.ARTIFACT_TREE,
            name,
            description,
            artifactIds,
            columns,
            new HashMap<>()
        );
    }
}
