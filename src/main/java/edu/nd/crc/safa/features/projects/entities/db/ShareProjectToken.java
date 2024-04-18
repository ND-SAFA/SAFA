package edu.nd.crc.safa.features.projects.entities.db;

import java.time.LocalDateTime;
import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Getter
@Setter
@Entity
@Table(name = "share_project_token")
public class ShareProjectToken {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.BINARY)
    @Column
    private UUID id;

    @JoinColumn(name = "project_id")
    @ManyToOne(fetch = FetchType.LAZY)
    @JdbcTypeCode(SqlTypes.BINARY)
    @OnDelete(action = OnDeleteAction.CASCADE)
    private Project project;

    @Column
    private LocalDateTime expiration;

    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Enumerated(EnumType.STRING)
    @Column
    private ProjectRole role;

    public ShareProjectToken(Project project, ProjectRole role) {
        this.project = project;
        this.role = role;
        this.expiration = LocalDateTime.now().plusWeeks(1);
    }

}
