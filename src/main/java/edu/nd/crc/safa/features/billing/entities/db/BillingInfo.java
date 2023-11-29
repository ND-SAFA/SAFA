package edu.nd.crc.safa.features.billing.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.db.Organization;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import jakarta.persistence.Version;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

/**
 * A database entity containing all billing related information for an organization
 */
@Entity
@Table(name = "billing_info")
@Getter
@Setter
@NoArgsConstructor
public class BillingInfo {

    @JdbcTypeCode(SqlTypes.BINARY)
    @Id
    @GeneratedValue
    @Column
    private UUID id;

    @Column
    private int balance;

    @Column
    private int totalUsed;

    @Column
    private int totalSuccessful;

    @JoinColumn(name = "organization_id")
    @OnDelete(action = OnDeleteAction.CASCADE)
    @OneToOne(fetch = FetchType.LAZY)
    private Organization organization;

    @Version
    private long version;

    public BillingInfo(Organization organization) {
        this.organization = organization;
    }
}
