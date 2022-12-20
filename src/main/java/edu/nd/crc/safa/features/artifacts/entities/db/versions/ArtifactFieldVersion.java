package edu.nd.crc.safa.features.artifacts.entities.db.versions;

import java.util.List;
import java.util.Objects;
import java.util.UUID;
import java.util.stream.Collectors;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.OneToMany;
import javax.persistence.OneToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactFieldStorageType;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactSchemaField;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.Hibernate;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "artifact_field_version")
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class ArtifactFieldVersion {
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column
    private UUID id;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "artifact_version_id", nullable = false)
    private ArtifactVersion artifactVersion;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "field_id", nullable = false)
    private ArtifactSchemaField schemaField;

    @Getter(AccessLevel.NONE)
    @Setter(AccessLevel.NONE)
    @OneToOne(mappedBy = "fieldVersion", fetch = FetchType.EAGER)
    private BooleanFieldValue booleanValue;

    @Getter(AccessLevel.NONE)
    @Setter(AccessLevel.NONE)
    @OneToOne(mappedBy = "fieldVersion", fetch = FetchType.EAGER)
    private FloatFieldValue floatValue;

    @Getter(AccessLevel.NONE)
    @Setter(AccessLevel.NONE)
    @OneToOne(mappedBy = "fieldVersion", fetch = FetchType.EAGER)
    private IntegerFieldValue intValue;

    @Getter(AccessLevel.NONE)
    @Setter(AccessLevel.NONE)
    @OneToOne(mappedBy = "fieldVersion", fetch = FetchType.EAGER)
    private StringFieldValue stringValue;

    @Getter(AccessLevel.NONE)
    @Setter(AccessLevel.NONE)
    @OneToMany(mappedBy = "fieldVersion", fetch = FetchType.EAGER)
    private List<StringArrayFieldValue> stringArrayValue;

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o)) {
            return false;
        }
        ArtifactFieldVersion that = (ArtifactFieldVersion) o;
        return id != null && Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }

    public ArtifactFieldStorageType getValueType() {
        return schemaField.getType().getStorageType();
    }

    public boolean getBooleanValue() {
        if (getValueType() != ArtifactFieldStorageType.BOOLEAN || booleanValue == null) {
            throw new NullPointerException("This artifact does not have a boolean value.");
        }
        return booleanValue.isValue();
    }

    public float getFloatValue() {
        if (getValueType() != ArtifactFieldStorageType.FLOAT || floatValue == null) {
            throw new NullPointerException("This artifact does not have a float value.");
        }
        return floatValue.getValue();
    }

    public int getIntegerValue() {
        if (getValueType() != ArtifactFieldStorageType.INTEGER || intValue == null) {
            throw new NullPointerException("This artifact does not have an int value.");
        }
        return intValue.getValue();
    }

    public String getStringValue() {
        if (getValueType() != ArtifactFieldStorageType.STRING || stringValue == null) {
            throw new NullPointerException("This artifact does not have a string value.");
        }
        return stringValue.getValue();
    }

    public List<String> getStringArrayValue() {
        if (getValueType() != ArtifactFieldStorageType.STRING_ARRAY || stringArrayValue == null) {
            throw new NullPointerException("This artifact does not have a string value.");
        }
        return stringArrayValue.stream().map(StringArrayFieldValue::getValue).collect(Collectors.toList());
    }
}
