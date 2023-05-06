package edu.nd.crc.safa.utilities.graphql.entities;

import java.lang.reflect.Field;
import java.util.List;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.ReflectionUtils;

public interface DefaultPaginatable extends Paginatable {

    @Override
    default void paginate(SafaUser user) {
        List<Field> fields = ReflectionUtils.getAllFields(this.getClass());
        fields.forEach(field -> {
            try {
                field.setAccessible(true);
                Object value = field.get(this);
                if (value instanceof Paginatable) {
                    ((Paginatable) value).paginate(user);
                }
            } catch (IllegalArgumentException | IllegalAccessException e) {
                e.printStackTrace();
            }
        });
    }
}
