package edu.nd.crc.safa.features.billing.services;

import java.util.UUID;

import edu.nd.crc.safa.features.billing.entities.db.Transaction;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.utilities.CachedValue;

import com.stripe.Stripe;
import com.stripe.exception.StripeException;
import com.stripe.model.Event;
import com.stripe.model.EventDataObjectDeserializer;
import com.stripe.model.Price;
import com.stripe.model.Product;
import com.stripe.model.StripeObject;
import com.stripe.model.checkout.Session;
import com.stripe.net.Webhook;
import com.stripe.param.ProductRetrieveParams;
import com.stripe.param.checkout.SessionCreateParams;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Service;

/**
 * An implementation of {@link IExternalBillingService} that
 * uses Stripe
 */
@Service
public class StripeService implements IExternalBillingService {
    private static final Logger logger = LoggerFactory.getLogger(StripeService.class);

    @Value("${stripe.success_url}")
    private String successUrl;

    @Value("${stripe.cancel_url}")
    private String cancelUrl;

    @Value("${stripe.credit_product_id}")
    private String creditProductId;

    @Value("${stripe.webhook_key}")
    private String webhookSecret;

    private final BillingService billingService;

    private final CachedValue<Price> priceOfCredit;

    public StripeService(@Value("${stripe.api_key}") String apiKey, @Lazy BillingService billingService) {
        this.billingService = billingService;

        if (apiKey != null && !apiKey.isBlank()) {
            Stripe.apiKey = apiKey;
        } else {
            logger.warn("No Stripe API key provided. Billing services will be unavailable. "
                + "Set the environment variable STRIPE_API_KEY to fix this issue.");
        }

        priceOfCredit = new CachedValue<>(this::retrieveCreditPriceFromStripe);
    }

    @Override
    public String startTransaction(Transaction transaction) {
        String referenceId = transaction.getId().toString();

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
                        .setQuantity((long) transaction.getAmount())
                        .setPrice(priceOfCredit.getValue().getId())
                        .build())
                .setClientReferenceId(transaction.getId().toString())
                .build();

        try {
            Session session = Session.create(params);
            transaction.setExternalReferenceId(session.getId());
            logger.info("Started transaction with reference ID {}", referenceId);
            return session.getUrl();
        } catch (StripeException e) {
            throw new SafaError("Failed to create Stripe session: %s", e.getMessage());
        }

    }

    @Override
    public void endTransaction(Transaction transaction) {
        logger.info("Finished transaction with reference ID {}", transaction.getId());
    }

    @Override
    public void cancelTransaction(Transaction transaction) {
        String sessionId = transaction.getExternalReferenceId();
        Session session = getSession(sessionId);
        if ("open".equals(session.getStatus())) {
            expireSession(session);
        }
        logger.info("Canceled transaction with reference ID {}", transaction.getId());
    }

    // This will get the price of a credit with caching so that many requests to the BE do not
    // spam Stripe with requests
    @Override
    public long getCreditPrice() {
        return priceOfCredit.getValue().getUnitAmount();
    }

    /**
     * As opposed to {@link #getCreditPrice()}, this actually goes to Stripe to retrieve the
     * price, without any caching
     *
     * @return The price of a credit according to stripe
     */
    private Price retrieveCreditPriceFromStripe() {
        try {
            ProductRetrieveParams params =
                ProductRetrieveParams.builder()
                    .addExpand("default_price")
                    .build();

            Product creditProduct = Product.retrieve(creditProductId, params, null);
            return creditProduct.getDefaultPriceObject();
        } catch (StripeException e) {
            throw new SafaError("Failed to retrieve credit price from Stripe", e);
        }
    }

    /**
     * Get a stripe session using the session ID
     *
     * @param sessionId The ID of the session
     * @return The session
     */
    private Session getSession(String sessionId) {
        try {
            return Session.retrieve(sessionId);
        } catch (StripeException e) {
            throw new SafaError("Failed to retrieve Stripe session", e);
        }
    }

    /**
     * Process a stripe webhook event
     *
     * @param eventBody The body of the webhook event
     * @param signatureHeader The stripe signature header from the event
     */
    public void processWebhookEvent(String eventBody, String signatureHeader) {
        Event event = parseEvent(eventBody, signatureHeader);
        StripeObject stripeObject = parseStripeObject(event);

        StripeEventType eventType = StripeEventType.fromApiName(event.getType());
        switch (eventType) {
            case SESSION_COMPLETED -> handleSessionCompletedEvent((Session) stripeObject);
            case SESSION_EXPIRED -> handleSessionExpiredEvent((Session) stripeObject);
            default -> logger.debug("Ignoring event of unknown type " + event.getType());
        }
    }

    /**
     * Cancel a session with the given ID by marking it as expired
     *
     * @param sessionId The ID of the session
     */
    public void cancelSession(String sessionId) {
        expireSession(getSession(sessionId));
    }

    /**
     * Mark a session as expired
     *
     * @param session The session
     */
    private void expireSession(Session session) {
        try {
            session.expire();
        } catch (StripeException e) {
            throw new SafaError("Failed to mark session as expired", e);
        }
    }

    /**
     * Parse the webhook body and signature to create a stripe event object
     *
     * @param eventBody The body of the webhook event
     * @param signatureHeader The stripe signature header from the event
     * @return The parsed stripe event
     */
    private Event parseEvent(String eventBody, String signatureHeader) {
        try {
            return Webhook.constructEvent(
                eventBody, signatureHeader, webhookSecret
            );
        }  catch (Exception e) {
            // Invalid signature
            throw new SafaError("Failed to validate stripe event", e);
        }
    }

    /**
     * Further parse the stripe event object to retrieve the stripe object containing the event details
     *
     * @param event The parsed stripe event
     * @return The stripe object containing event details
     */
    private StripeObject parseStripeObject(Event event) {
        EventDataObjectDeserializer dataObjectDeserializer = event.getDataObjectDeserializer();
        if (dataObjectDeserializer.getObject().isPresent()) {
            return dataObjectDeserializer.getObject().get();
        } else {
            throw new SafaError("Failed to parse object");
        }
    }

    /**
     * Handle the stripe session completed event
     *
     * @param session The session object contained in the event
     */
    private void handleSessionCompletedEvent(Session session) {
        UUID transactionId = UUID.fromString(session.getClientReferenceId());
        billingService.endTransaction(transactionId);
    }

    /**
     * Handle the stripe session expired event
     *
     * @param session The session that expired
     */
    private void handleSessionExpiredEvent(Session session) {
        UUID transactionId = UUID.fromString(session.getClientReferenceId());
        billingService.cancelTransaction(transactionId);
    }

    @Getter
    @AllArgsConstructor
    private enum StripeEventType {
        SESSION_COMPLETED("checkout.session.completed"),
        SESSION_EXPIRED("checkout.session.expired"),
        UNKNOWN("");

        private final String apiName;

        public static StripeEventType fromApiName(String apiName) {
            for (StripeEventType eventType : StripeEventType.values()) {
                if (eventType.getApiName().isEmpty()) {
                    continue;
                }
                if (eventType.getApiName().equals(apiName)) {
                    return eventType;
                }
            }
            return UNKNOWN;
        }
    }
}
