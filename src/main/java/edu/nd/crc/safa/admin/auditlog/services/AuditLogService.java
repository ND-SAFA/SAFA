package edu.nd.crc.safa.admin.auditlog.services;

import java.time.LocalDateTime;
import java.util.List;

import edu.nd.crc.safa.admin.auditlog.entities.db.AuditLogEntry;
import edu.nd.crc.safa.admin.auditlog.repositories.AuditLogRepository;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class AuditLogService {

    private final AuditLogRepository auditLogRepo;

    public List<AuditLogEntry> getBetween(LocalDateTime before, LocalDateTime after) {
        List<AuditLogEntry> data = auditLogRepo.findByTimestampBetweenOrderByTimestampDesc(before, after);
        System.out.println(data);
        System.out.println(auditLogRepo.findAll());
        return data;
    }

    public List<AuditLogEntry> getBefore(LocalDateTime before) {
        return getBetween(before, LocalDateTime.MIN);
    }

    public List<AuditLogEntry> getAfter(LocalDateTime after) {
        return getBetween(LocalDateTime.MAX, after);
    }

    public List<AuditLogEntry> getAll() {
        return getAfter(LocalDateTime.MIN);
    }

    public AuditLogEntry createEntry(SafaUser user, String message) {
        return auditLogRepo.save(new AuditLogEntry(user, message));
    }
}
