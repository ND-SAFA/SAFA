package edu.nd.crc.safa.features.github.entities.events;

import java.time.LocalDateTime;

import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Getter;
import org.springframework.context.ApplicationEvent;

@Getter
public class ProjectSummarizedEvent extends ApplicationEvent {

    private final LocalDateTime summarizedTime;
    private final SafaUser user;
    private final Project project;

    public ProjectSummarizedEvent(Object source, SafaUser user, Project project) {
        super(source);
        this.summarizedTime = LocalDateTime.now();
        this.user = user;
        this.project = project;
    }
}
