package edu.nd.crc.safa.features.artifacts.entities.db.versions;

import java.util.Objects;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.Lob;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.common.ServiceProvider;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.Hibernate;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "string_array_field_value")
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class StringArrayFieldValue implements IFieldValue {
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column
    private UUID id;

    @Lob
    @Column(name = "field_value", nullable = false)
    private String value;

    @ManyToOne
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
        StringArrayFieldValue that = (StringArrayFieldValue) o;
        return id != null && Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }

    @Override
    public void setValueFromString(String strValue) {
        setValue(strValue);
    }

    @Override
    public String getValueAsString() {
        return getValue();
    }

    @Override
    public void save(ServiceProvider serviceProvider) {
        serviceProvider.getStringArrayFieldValueRepository().save(this);
    }
}
