package edu.nd.crc.safa.features.notifications;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Data;

@Data
public class ProjectNotification {
    private List<SafaUser> users = new ArrayList<>();
}
