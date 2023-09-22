package edu.nd.crc.safa.test.features.jobs;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.entities.jobs.HGenJob;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

class TestJobMessage extends ApplicationBaseTest {
    @Autowired
    JobService jobService;
    @Autowired
    SafaUserService userService;

    @Disabled
    @Test
    void testSubscribe() throws Exception {
        String clientId = "client_id";
        JobDbEntity jobDbEntity = jobService.createNewJobForUser(HGenJob.class, "hgen", currentUser);

        notificationService.createNewConnection(clientId);
        notificationService.subscribeToJob(clientId, jobDbEntity);
        String changeMessage = notificationService.getMessageInQueue(clientId);
    }
}
