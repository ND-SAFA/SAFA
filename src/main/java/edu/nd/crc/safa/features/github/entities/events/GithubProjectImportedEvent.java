package edu.nd.crc.safa.features.github.entities.events;

import java.time.LocalDateTime;

import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Getter;
import org.springframework.context.ApplicationEvent;

@Getter
public class GithubProjectImportedEvent extends ApplicationEvent {
    private final LocalDateTime importedTime;
    private final SafaUser user;
    private final Project project;
    private final GithubIdentifier githubIdentifier;

    public GithubProjectImportedEvent(Object source, SafaUser user, Project project,
                                      GithubIdentifier githubIdentifier) {
        super(source);
        this.importedTime = LocalDateTime.now();
        this.user = user;
        this.project = project;
        this.githubIdentifier = githubIdentifier;
    }
}
