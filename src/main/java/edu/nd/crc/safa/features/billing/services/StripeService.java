package edu.nd.crc.safa.features.billing.services;

import com.stripe.net.RequestOptions;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

/**
 * An implementation of {@link IBillingService} that
 * uses Stripe
 */
@Service
public class StripeService implements IBillingService {
    private static final Logger logger = LoggerFactory.getLogger(StripeService.class);

    private final RequestOptions requestOptions;

    public StripeService(@Value("${stripe.api_key}") String apiKey) {
        requestOptions = buildRequestOptions(apiKey);
    }

    private RequestOptions buildRequestOptions(String apiKey) {
        RequestOptions.RequestOptionsBuilder builder = RequestOptions.builder();

        if (apiKey != null && !apiKey.isBlank()) {
            builder.setApiKey(apiKey);
        } else {
            logger.warn("No Stripe API key provided. Billing services will be unavailable. "
                + "Set the environment variable STRIPE_API_KEY to fix this issue.");
        }

        return builder.build();
    }

    @Override
    public void startTransaction(String referenceId) {
        logger.info("Starting transaction with reference ID {}", referenceId);
    }

    @Override
    public void endTransaction(String referenceId) {
        logger.info("Ending transaction with reference ID {}", referenceId);
    }
}
