package edu.nd.crc.safa.features.jobs.controllers;

import java.util.UUID;

import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.services.JobService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.DestinationVariable;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.simp.SimpMessageHeaderAccessor;
import org.springframework.stereotype.Controller;

@Controller
public class JobMessageController {

    @Autowired
    JobService jobService;

    @MessageMapping("/jobs/{jobId}")
    public void sendJobState(@DestinationVariable UUID jobId, SimpMessageHeaderAccessor headerAccessor) {
        JobAppEntity job = JobAppEntity.createFromJob(jobService.getJobById(jobId));
//        String userDestination = "/user/:userId";
//        messagingTemplate.convertAndSend(userDestination, "Subscribed to job updates for job " + jobId);
    }
}
