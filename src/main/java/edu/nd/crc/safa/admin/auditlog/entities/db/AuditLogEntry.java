package edu.nd.crc.safa.admin.auditlog.entities.db;

import java.time.LocalDateTime;
import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.Lob;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Entity
@Table(name = "audit_log")
@Getter
@Setter
@NoArgsConstructor
public class AuditLogEntry {
    @JdbcTypeCode(SqlTypes.BINARY)
    @Id
    @GeneratedValue
    @Column(nullable = false)
    private UUID id;

    @Column(name = "time")
    private LocalDateTime timestamp;

    @Lob
    @Column(columnDefinition = "mediumtext")
    private String entry;

    @JoinColumn(name = "user_id")
    @OnDelete(action = OnDeleteAction.NO_ACTION)
    @ManyToOne
    private SafaUser user;

    public AuditLogEntry(SafaUser user, String message) {
        this.user = user;
        this.entry = message;
        this.timestamp = LocalDateTime.now();
    }
}
