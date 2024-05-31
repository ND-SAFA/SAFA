package edu.nd.crc.safa.features.attributes.entities.db.definitions;

import java.util.UUID;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.attributes.entities.CustomAttributeType;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

@Entity
@Table(name = "custom_attribute",
    uniqueConstraints = {
        @UniqueConstraint(columnNames = {"keyname", "project_id"},
            name = AppConstraints.UNIQUE_KEYNAME_PER_PROJECT)
    }
)
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class CustomAttribute {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column
    private UUID id;

    @Column(nullable = false)
    @JdbcTypeCode(SqlTypes.INTEGER)
    @Enumerated(EnumType.ORDINAL)
    private CustomAttributeType type;

    @Column(nullable = false)
    private String keyname;

    @Column(nullable = false)
    private String label;

    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(nullable = false)
    private UUID projectId;

}
