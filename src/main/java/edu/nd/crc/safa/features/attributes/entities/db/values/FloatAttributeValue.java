package edu.nd.crc.safa.features.attributes.entities.db.values;

import java.util.Optional;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.attributes.repositories.values.FloatAttributeValueRepository;
import edu.nd.crc.safa.features.attributes.services.AttributeSystemServiceProvider;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "float_attribute_value")
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class FloatAttributeValue implements IAttributeValue {
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column
    private UUID id;

    @Column(name = "attribute_value", nullable = false)
    private float value;

    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "attribute_version_id", nullable = false)
    private ArtifactAttributeVersion attributeVersion;

    @Override
    public void setValueFromString(String strValue) {
        setValue(Float.parseFloat(strValue));
    }

    @Override
    public String getValueAsString() {
        return Float.toString(getValue());
    }

    @Override
    public void save(AttributeSystemServiceProvider serviceProvider) {
        FloatAttributeValueRepository repo = serviceProvider.getFloatAttributeValueRepository();
        Optional<FloatAttributeValue> existing = repo.getByAttributeVersion(this.attributeVersion);
        existing.ifPresent(value -> this.id = value.getId());
        repo.save(this);
    }
}
