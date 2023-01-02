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

import edu.nd.crc.safa.features.attributes.repositories.values.BooleanAttributeValueRepository;
import edu.nd.crc.safa.features.attributes.services.AttributeSystemServiceProvider;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "boolean_attribute_value")
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class BooleanAttributeValue implements IAttributeValue {
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column
    private UUID id;

    @Column(name = "attribute_value", nullable = false)
    private boolean value;

    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "attribute_version_id", nullable = false)
    private ArtifactAttributeVersion attributeVersion;

    @Override
    public void setValueFromString(String strValue) {
        setValue(Boolean.parseBoolean(strValue));
    }

    @Override
    public String getValueAsString() {
        return Boolean.toString(isValue());
    }

    @Override
    public void save(AttributeSystemServiceProvider serviceProvider) {
        BooleanAttributeValueRepository repo = serviceProvider.getBooleanAttributeValueRepository();
        Optional<BooleanAttributeValue> existing = repo.getByAttributeVersion(this.attributeVersion);
        existing.ifPresent(booleanAttributeValue -> this.id = booleanAttributeValue.getId());
        repo.save(this);
    }
}
