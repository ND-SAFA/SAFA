package features.notifications.documents;

/**
 * Test that creating a document sends notification containing:
 * - single change
 * - change entity is DOCUMENT
 * - change action is UPDATE
 * - change contains Document.id
 */
public class TestCreateNotification extends AbstractDocumentNotificationTest {

    @Override
    protected void performAction() throws Exception {
        this.createDocument();
    }
}
