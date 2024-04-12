package edu.nd.crc.safa.features.github.entities.events;

import java.time.LocalDateTime;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Getter;
import org.springframework.context.ApplicationEvent;

@Getter
public class GithubLinkedEvent extends ApplicationEvent {

    private final LocalDateTime linkedTime;
    private final SafaUser user;

    public GithubLinkedEvent(Object source, SafaUser user) {
        super(source);
        this.linkedTime = LocalDateTime.now();
        this.user = user;
    }
}
