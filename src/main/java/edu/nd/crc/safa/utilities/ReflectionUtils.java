package edu.nd.crc.safa.utilities;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.List;

public interface ReflectionUtils {

    /**
     * Get all fields from a class, including inherited fields.
     *
     * @param clazz The class to get fields from.
     * @return A list of all fields in the class.
     */
    static List<Field> getAllFields(Class<?> clazz) {
        List<Field> fields = new ArrayList<>();
        do {
            fields.addAll(List.of(clazz.getDeclaredFields()));
            clazz = clazz.getSuperclass();
        } while (clazz.getSuperclass() != null);
        return fields;
    }
}
