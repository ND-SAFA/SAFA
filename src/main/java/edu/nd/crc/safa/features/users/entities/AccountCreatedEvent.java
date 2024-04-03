package edu.nd.crc.safa.features.users.entities;

import java.time.LocalDateTime;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Getter;
import lombok.Setter;
import org.springframework.context.ApplicationEvent;

@Getter
@Setter
public class AccountCreatedEvent extends ApplicationEvent {

    private SafaUser user;
    private LocalDateTime createdTime;

    public AccountCreatedEvent(Object source, SafaUser user) {
        super(source);
        this.user = user;
        this.createdTime = LocalDateTime.now();
    }
}
