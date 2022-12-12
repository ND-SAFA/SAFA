package edu.nd.crc.safa.features.artifacts.entities.db.schema;

import java.util.Objects;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactFieldType;
import edu.nd.crc.safa.features.types.ArtifactType;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.Hibernate;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "artifact_schema_field",
    uniqueConstraints = {
        @UniqueConstraint(columnNames = {"keyname", "artifact_type_id"},
            name = AppConstraints.UNIQUE_KEYNAME_PER_ARTIFACT_TYPE)
    }
)
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class ArtifactSchemaField {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column
    private UUID id;

    @Column(nullable = false)
    @Enumerated(EnumType.ORDINAL)
    private ArtifactFieldType type;

    @Column(nullable = false)
    private String key;

    @Column(nullable = false)
    private String label;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "artifact_type_id", nullable = false)
    private ArtifactType artifact;

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o)) {
            return false;
        }
        ArtifactSchemaField that = (ArtifactSchemaField) o;
        return id != null && Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }
}
