package edu.nd.crc.safa.features.billing.services;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import com.stripe.Stripe;
import com.stripe.exception.StripeException;
import com.stripe.model.checkout.Session;
import com.stripe.param.checkout.SessionCreateParams;
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

    @Value("${stripe.success_url}")
    private String successUrl;

    @Value("${stripe.cancel_url}")
    private String cancelUrl;

    @Value("${stripe.credit_product_key}")
    private String creditProductKey;

    public StripeService(@Value("${stripe.api_key}") String apiKey) {
        if (apiKey != null && !apiKey.isBlank()) {
            Stripe.apiKey = apiKey;
        } else {
            logger.warn("No Stripe API key provided. Billing services will be unavailable. "
                + "Set the environment variable STRIPE_API_KEY to fix this issue.");
        }
    }

    @Override
    public String startTransaction(String referenceId) {
        logger.info("Starting transaction with reference ID {}", referenceId);

        SessionCreateParams params =
            SessionCreateParams.builder()
                .setMode(SessionCreateParams.Mode.PAYMENT)
                .setSuccessUrl(successUrl)
                .setCancelUrl(cancelUrl)
                .setAutomaticTax(
                    SessionCreateParams.AutomaticTax.builder()
                        .setEnabled(true)
                        .build())
                .addLineItem(
                    SessionCreateParams.LineItem.builder()
                        .setQuantity(1L)
                        // Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        .setPrice(creditProductKey)
                        .build())
                .build();

        try {
            Session session = Session.create(params);
            return session.getUrl();
        } catch (StripeException e) {
            throw new SafaError("Failed to create Stripe session: %s", e.getMessage());
        }

    }

    @Override
    public void endTransaction(String referenceId) {
        logger.info("Ending transaction with reference ID {}", referenceId);
    }
}
