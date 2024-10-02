package edu.nd.crc.safa.admin.auditlog.entities.app;

import java.time.LocalDateTime;

import edu.nd.crc.safa.admin.auditlog.entities.db.AuditLogEntry;

import lombok.Data;

@Data
public class AuditLogEntryDTO {
    private LocalDateTime timestamp;
    private String entry;
    private String user;

    public AuditLogEntryDTO(AuditLogEntry log) {
        this.timestamp = log.getTimestamp();
        this.entry = log.getEntry();
        this.user = log.getUserEmail();
    }
}
