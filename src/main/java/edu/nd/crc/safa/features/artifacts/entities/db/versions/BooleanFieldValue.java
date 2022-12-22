package edu.nd.crc.safa.features.artifacts.entities.db.versions;

import java.util.Objects;
import java.util.Optional;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.artifacts.repositories.versions.BooleanFieldValueRepository;
import edu.nd.crc.safa.features.artifacts.services.ArtifactSystemServiceProvider;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.Hibernate;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "boolean_field_value")
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class BooleanFieldValue implements IFieldValue {
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column
    private UUID id;

    @Column(name = "field_value", nullable = false)
    private boolean value;

    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "field_version_id", nullable = false)
    private ArtifactFieldVersion fieldVersion;

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || Hibernate.getClass(this) != Hibernate.getClass(o)) {
            return false;
        }
        BooleanFieldValue that = (BooleanFieldValue) o;
        return id != null && Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }

    @Override
    public void setValueFromString(String strValue) {
        setValue(Boolean.parseBoolean(strValue));
    }

    @Override
    public String getValueAsString() {
        return Boolean.toString(isValue());
    }

    @Override
    public void save(ArtifactSystemServiceProvider serviceProvider) {
        BooleanFieldValueRepository repo = serviceProvider.getBooleanFieldValueRepository();
        Optional<BooleanFieldValue> existing = repo.getByFieldVersion(this.fieldVersion);
        existing.ifPresent(booleanFieldValue -> this.id = booleanFieldValue.getId());
        repo.save(this);
    }
}
