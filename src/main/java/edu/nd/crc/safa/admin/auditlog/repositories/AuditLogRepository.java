package edu.nd.crc.safa.admin.auditlog.repositories;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.admin.auditlog.entities.db.AuditLogEntry;

import org.springframework.data.repository.CrudRepository;

public interface AuditLogRepository extends CrudRepository<AuditLogEntry, UUID> {
    List<AuditLogEntry> findByTimestampBetweenOrderByTimestampDesc(LocalDateTime timestampBefore, LocalDateTime timestampAfter);
}
