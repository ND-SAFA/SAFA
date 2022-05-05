package edu.nd.crc.safa.server.controllers;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Job;
import edu.nd.crc.safa.server.repositories.JobRepository;
import edu.nd.crc.safa.server.services.NotificationService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.DestinationVariable;
import org.springframework.messaging.simp.annotation.SubscribeMapping;
import org.springframework.stereotype.Controller;

@Controller
public class WebsocketController {
    JobRepository jobRepository;
    NotificationService notificationService;

    @Autowired
    public WebsocketController(JobRepository jobRepository,
                               NotificationService notificationService) {
        this.jobRepository = jobRepository;
        this.notificationService = notificationService;
    }

    @SubscribeMapping("/jobs/{jobId}")
    public Job chat(@DestinationVariable UUID jobId) throws SafaError {
        System.out.println("Subscriber mapping!");
        Optional<Job> jobOption = this.jobRepository.findById(jobId);
        if (jobOption.isPresent()) {
            System.out.println("Returning job message!");
            return jobOption.get();
        }
        throw new SafaError("Could not find job with id:" + jobId);
    }
}
