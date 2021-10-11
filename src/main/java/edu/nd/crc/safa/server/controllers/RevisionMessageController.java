package edu.nd.crc.safa.server.controllers;

import java.util.UUID;

import edu.nd.crc.safa.server.db.repositories.ProjectVersionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.DestinationVariable;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Controller;

@Controller
public class RevisionMessageController {

    private final SimpMessagingTemplate template;

    @Autowired
    public RevisionMessageController(SimpMessagingTemplate template,
                                     ProjectVersionRepository projectVersionRepository) {
        this.template = template;
    }


    @MessageMapping("/revisions/{versionId}")
    public void handleRevisionMessage(String revision, @DestinationVariable UUID versionId) throws Exception {
        System.out.println("RECEIVED REVISION MESSAGE");
        String destination = String.format("/topic/revisions/%s", versionId);
        template.convertAndSend(destination, revision);
    }
}
