package edu.nd.crc.safa.features.permissions.checks.utility;

import java.util.function.Function;

import edu.nd.crc.safa.features.permissions.checks.AdditionalPermissionCheck;
import edu.nd.crc.safa.features.permissions.checks.PermissionCheckContext;

/**
 * An additional permission check which compares two values
 *
 * @param <T> The type of object being compared
 */
public class ComparisonCheck<T extends Comparable<T>> implements AdditionalPermissionCheck {

    private final Function<PermissionCheckContext, T> valueSupplier;
    private final Function<PermissionCheckContext, T> compareValueSupplier;
    private final ComparisonType comparisonType;

    /**
     * Compare two values by suppliers
     *
     * @param valueSupplier The supplier of the main value. This should be the value associated with the project,
     *                      organization, etc
     * @param compareValueSupplier The supplier of the comparison value. This is the value that the main value
     *                             is being compared against
     * @param comparisonType The type of comparison
     */
    public ComparisonCheck(Function<PermissionCheckContext, T> valueSupplier,
                           Function<PermissionCheckContext, T> compareValueSupplier,
                           ComparisonType comparisonType) {
        this.valueSupplier = valueSupplier;
        this.compareValueSupplier = compareValueSupplier;
        this.comparisonType = comparisonType;
    }

    /**
     * Compare against a constant value
     *
     * @param valueSupplier The supplier of the main value. This should be the value associated with the project,
     *                      organization, etc
     * @param compareValue The constant value to compare against
     * @param comparisonType The type of comparison
     */
    public ComparisonCheck(Function<PermissionCheckContext, T> valueSupplier,
                           T compareValue, ComparisonType comparisonType) {
        this(valueSupplier, context -> compareValue, comparisonType);
    }

    @Override
    public boolean doCheck(PermissionCheckContext context) {
        T value = valueSupplier.apply(context);
        T comparisonValue = compareValueSupplier.apply(context);
        int comparison = value.compareTo(comparisonValue);

        return switch (comparisonType) {
            case LESS -> comparison < 0;
            case LESS_OR_EQUAL -> comparison <= 0;
            case GREATER -> comparison > 0;
            case GREATER_OR_EQUAL -> comparison >= 0;
            case EQUAL -> comparison == 0;
        };
    }

    /**
     * The type of comparison to perform
     */
    public enum ComparisonType {
        LESS,
        LESS_OR_EQUAL,
        GREATER,
        GREATER_OR_EQUAL,
        EQUAL
    }
}
