package edu.nd.crc.safa.features.billing.controllers;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.billing.services.BillingService;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import com.stripe.model.Event;
import com.stripe.model.EventDataObjectDeserializer;
import com.stripe.model.StripeObject;
import com.stripe.model.checkout.Session;
import com.stripe.net.Webhook;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;

@Controller
public class TempStripeController extends BaseController {

    private final BillingService billingService;
    private final OrganizationService organizationService;

    @Value("${stripe.webhook_secret")
    private String webhookSecret;

    public TempStripeController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                                BillingService billingService, OrganizationService organizationService) {
        super(resourceBuilder, serviceProvider);
        this.billingService = billingService;
        this.organizationService = organizationService;
    }

    @GetMapping(AppRoutes.Stripe.CHECKOUT)
    public String getCheckoutUrl(@PathVariable int amount) {
        Organization organization = organizationService.getPersonalOrganization(getCurrentUser());
        return billingService.startTransaction(organization, amount, "Test transaction");
    }

    @PostMapping(AppRoutes.Stripe.WEBHOOK)
    public void processEvent(@RequestBody String body,
                             @RequestHeader("Stripe-Signature") String stripeSignature) {
        Event event = null;
        String endpointSecret = "whsec_83635b556e9fe43e6573a4153852c9a150a9924c302b746f383f7b915298c6e9";
        try {
            event = Webhook.constructEvent(
                body, stripeSignature, endpointSecret
            );
        }  catch (Exception e) {
            // Invalid signature
            throw new SafaError("Failed", e);
        }

        // Deserialize the nested object inside the event
        EventDataObjectDeserializer dataObjectDeserializer = event.getDataObjectDeserializer();
        StripeObject stripeObject = null;
        if (dataObjectDeserializer.getObject().isPresent()) {
            stripeObject = dataObjectDeserializer.getObject().get();
        } else {
            // Deserialization failed, probably due to an API version mismatch.
            // Refer to the Javadoc documentation on `EventDataObjectDeserializer` for
            // instructions on how to handle this case, or return an error here.
            throw new SafaError("Failed to parse object");
        }

        if ("checkout.session.completed".equals(event.getType())) {
            billingService.endTransaction(((Session) stripeObject).getClientReferenceId());
        }


    }
}
