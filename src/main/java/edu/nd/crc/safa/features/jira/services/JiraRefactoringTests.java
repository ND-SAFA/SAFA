package edu.nd.crc.safa.features.jira.services;

import lombok.AllArgsConstructor;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
public class JiraRefactoringTests {

    private JiraConnectionService service;

    @EventListener(ApplicationReadyEvent.class)
    private void init() {

    }
}
