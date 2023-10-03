package edu.nd.crc.safa.test.features.notifications.documentartifact;

import edu.nd.crc.safa.test.services.CommitTestService;
import edu.nd.crc.safa.test.services.MessageVerificationTestService;
import edu.nd.crc.safa.test.services.assertions.VerificationTestSerfice;
import edu.nd.crc.safa.test.services.notifications.NotificationTestService;

import lombok.AllArgsConstructor;

@AllArgsConstructor
public class DocumentArtifactNotificationTestService {
    CommitTestService commitService;
    NotificationTestService notificationService;
    MessageVerificationTestService changeMessageVerifies;
    VerificationTestSerfice assertionService;


}
