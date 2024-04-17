package edu.nd.crc.safa.features.generation;

import java.time.LocalDateTime;

import edu.nd.crc.safa.features.generation.hgen.HGenRequest;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.Getter;
import org.springframework.context.ApplicationEvent;

@Getter
public class GenerationPerformedEvent extends ApplicationEvent {
    private final LocalDateTime performedTime;
    private final SafaUser user;
    private final ProjectVersion projectVersion;
    private final HGenRequest hGenRequest;

    public GenerationPerformedEvent(Object source, SafaUser user, ProjectVersion projectVersion,
                                    HGenRequest hGenRequest) {
        super(source);
        this.hGenRequest = hGenRequest;
        this.performedTime = LocalDateTime.now();
        this.user = user;
        this.projectVersion = projectVersion;
    }
}
