package unit.entities;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Set;

import javax.persistence.metamodel.EntityType;

import org.junit.jupiter.api.Test;
import unit.SpringBootBaseTest;

/**
 * Tests that the session to the test database
 * is active and that all entities are scanned.
 */
public class HibernateConnection extends SpringBootBaseTest {

    @Test
    public void entitiesScanned() {
        Set<EntityType<?>> entities = this.entityManager.getEntityManagerFactory().getMetamodel().getEntities();
        assertThat(entities.size()).isGreaterThanOrEqualTo(8);
    }
}
