package edu.nd.crc.safa.features.permissions.checks.config;

import java.util.function.Function;

import edu.nd.crc.safa.features.permissions.checks.PermissionCheckContext;
import edu.nd.crc.safa.features.permissions.checks.utility.ComparisonCheck;

/**
 * A specialization of {@link ComparisonCheck} which compares against a value in our configuration
 *
 * @param <T> The type of the configuration value
 */
public abstract class ConfigurationComparisonCheck<T extends Comparable<T>> extends ComparisonCheck<T> {
    /**
     * Constructor
     *
     * @param valueSupplier Function to supply the value where are checking
     * @param configKey Key for the configuration value
     * @param targetType Type of the configuration value
     * @param comparisonType Type of comparison to perform
     */
    public ConfigurationComparisonCheck(Function<PermissionCheckContext, T> valueSupplier, String configKey,
                                        Class<T> targetType, ComparisonType comparisonType) {
        super(valueSupplier, context -> getConfigValue(context, configKey, targetType), comparisonType);
    }

    /**
     * Gets a value from the configuration
     *
     * @param context The permission check context we're operating in
     * @param key The key for the configuration value
     * @param targetType The type of the configuration value
     * @param <T> The type of the configuration value
     * @return The value of the config variable, or null if it doesn't exist
     */
    private static <T extends Comparable<T>> T getConfigValue(PermissionCheckContext context, String key,
                                                              Class<T> targetType) {
        return context.getServiceProvider().getEnvironment().getProperty(key, targetType);
    }
}
