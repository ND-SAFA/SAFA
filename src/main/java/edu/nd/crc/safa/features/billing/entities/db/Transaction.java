package edu.nd.crc.safa.features.billing.entities.db;

import java.time.LocalDateTime;
import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.db.Organization;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.JdbcType;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;
import org.hibernate.type.descriptor.jdbc.VarcharJdbcType;

@Entity
@Table(name = "transaction")
@Getter
@Setter
@NoArgsConstructor
public class Transaction {

    public enum Status {
        PENDING,
        SUCCESSFUL,
        FAILED,
        CANCELED
    }

    @JdbcTypeCode(SqlTypes.BINARY)
    @Id
    @GeneratedValue
    @Column
    private UUID id;

    @Column
    @Enumerated(EnumType.STRING)
    @JdbcType(VarcharJdbcType.class)
    private Status status;

    @Column
    private int amount;

    @Column
    private String description;

    @Column
    private LocalDateTime timestamp;

    @JoinColumn(name = "organization_id")
    @OnDelete(action = OnDeleteAction.CASCADE)
    @OneToOne(fetch = FetchType.LAZY)
    private Organization organization;

    @Column
    private String externalReferenceId;

    public Transaction(int amount, String description, Organization organization) {
        this.amount = amount;
        this.description = description;
        this.status = Status.PENDING;
        this.timestamp = LocalDateTime.now();
        this.organization = organization;
        this.externalReferenceId = null;
    }

    public Transaction(int amount, String description, Organization organization, String externalReferenceId) {
        this(amount, description, organization);
        this.externalReferenceId = externalReferenceId;
    }

}
