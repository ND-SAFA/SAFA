package edu.nd.crc.safa.features.notifications.builders;

import java.util.List;

import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.IUser;

public class UserChangeBuilder extends AbstractEntityChangeBuilder<UserChangeBuilder> {
    protected UserChangeBuilder(IUser user) {
        super(user.getUserId());
        this.getEntityChangeMessage().setTopic(TopicCreator.getUserTopic(user.getUserId()));
    }

    public UserChangeBuilder withProjectUpdate(Project project) {
        return withEntitiesUpdate(NotificationEntity.PROJECT, List.of(project));
    }

    @Override
    protected UserChangeBuilder self() {
        return this;
    }
}
