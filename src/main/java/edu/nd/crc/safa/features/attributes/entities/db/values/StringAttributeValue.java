package edu.nd.crc.safa.features.attributes.entities.db.values;

import java.util.Optional;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.Lob;
import javax.persistence.OneToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.attributes.repositories.values.StringAttributeValueRepository;
import edu.nd.crc.safa.features.attributes.services.AttributeSystemServiceProvider;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.TextNode;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "string_attribute_value")
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class StringAttributeValue implements IAttributeValue {
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column
    private UUID id;

    @Lob
    @Column(name = "attribute_value", nullable = false, columnDefinition = "mediumtext")
    private String value;

    @OneToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "attribute_version_id", nullable = false)
    private ArtifactAttributeVersion attributeVersion;

    @Override
    public void setValueFromJsonNode(JsonNode jsonValue) {
        setValue(jsonValue.textValue());
    }

    @Override
    public JsonNode getValueAsJsonNode() {
        return TextNode.valueOf(getValue());
    }

    @Override
    public void save(AttributeSystemServiceProvider serviceProvider) {
        StringAttributeValueRepository repo = serviceProvider.getStringAttributeValueRepository();
        Optional<StringAttributeValue> existing = repo.getByAttributeVersion(this.attributeVersion);
        existing.ifPresent(value -> this.id = value.getId());
        repo.save(this);
    }
}
