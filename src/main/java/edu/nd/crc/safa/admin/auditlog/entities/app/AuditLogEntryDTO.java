package edu.nd.crc.safa.admin.auditlog.entities.app;

import java.time.LocalDateTime;

import edu.nd.crc.safa.admin.auditlog.entities.db.AuditLogEntry;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;

import lombok.Data;

@Data
public class AuditLogEntryDTO {
    private LocalDateTime timestamp;
    private String entry;
    private UserAppEntity user;

    public AuditLogEntryDTO(AuditLogEntry log) {
        this.timestamp = log.getTimestamp();
        this.entry = log.getEntry();
        this.user = new UserAppEntity(log.getUser());
    }
}
