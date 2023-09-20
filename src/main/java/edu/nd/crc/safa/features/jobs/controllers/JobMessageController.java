package edu.nd.crc.safa.features.jobs.controllers;

import java.util.UUID;

import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.services.JobService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.DestinationVariable;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.simp.SimpMessageHeaderAccessor;
import org.springframework.messaging.simp.annotation.SendToUser;
import org.springframework.stereotype.Controller;

@Controller
public class JobMessageController {

    @Autowired
    JobService jobService;

    @MessageMapping("/jobs/{jobId}")
    @SendToUser("/queue/job-updates")
    public JobAppEntity sendJobState(@DestinationVariable UUID jobId, SimpMessageHeaderAccessor headerAccessor) {
        // TODO: How to send message back to user?
        // User has to be subscribed to a topic to receive messages.
        // Create user channels?
        // User channels; receive any custom messages.

        // What does custom mean?
        // GenericMessage.
        // EntityChangeNotification
        // JobUpdate
        // UserUpdate
        return JobAppEntity.createFromJob(jobService.getJobById(jobId));
    }
}
