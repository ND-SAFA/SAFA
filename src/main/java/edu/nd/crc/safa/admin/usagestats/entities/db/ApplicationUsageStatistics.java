package edu.nd.crc.safa.admin.usagestats.entities.db;

import java.time.LocalDateTime;
import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
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
@Table(name = "usage_statistics")  // TODO
@Getter
@Setter
@NoArgsConstructor
public class ApplicationUsageStatistics {
    @JdbcTypeCode(SqlTypes.BINARY)
    @Id
    @GeneratedValue
    @Column
    private UUID id;

    @JoinColumn(name = "user_id")
    @OnDelete(action = OnDeleteAction.CASCADE)
    @ManyToOne
    private SafaUser user;

    @Column
    private int projectImports;

    @Column
    private int projectSummarizations;

    @Column
    private int projectGenerations;

    @Column
    private int linesGeneratedOn;

    @Column
    private LocalDateTime accountCreated;

    @Column
    private LocalDateTime githubLinked;

    @Column
    private LocalDateTime projectImported;

    @Column
    private LocalDateTime generated;
}
