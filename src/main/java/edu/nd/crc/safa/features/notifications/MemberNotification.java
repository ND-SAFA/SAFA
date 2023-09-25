package edu.nd.crc.safa.features.notifications;

import java.util.List;

import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class MemberNotification implements NotificationMessage {
    private final String entityType = "members";
    private List<UserAppEntity> entity;
}
