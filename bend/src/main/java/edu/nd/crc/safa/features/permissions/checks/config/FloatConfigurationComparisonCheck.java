package edu.nd.crc.safa.features.permissions.checks.config;

import java.util.function.Function;

import edu.nd.crc.safa.features.permissions.checks.PermissionCheckContext;

/**
 * Specialization of {@link ConfigurationComparisonCheck} for floats
 */
public abstract class FloatConfigurationComparisonCheck extends ConfigurationComparisonCheck<Double> {
    public FloatConfigurationComparisonCheck(Function<PermissionCheckContext, Double> valueSupplier, String configKey,
                                             ComparisonType comparisonType) {
        super(valueSupplier, configKey, Double.class, comparisonType);
    }
}
