package unit.entities;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Set;

import javax.persistence.metamodel.EntityType;

import org.hibernate.Session;
import org.junit.jupiter.api.Test;
import unit.SpringBootBaseTest;

/**
 * Tests that the session to the test database
 * is active and that all entities are scanned.
 */
public class HibernateConnection extends SpringBootBaseTest {

    @Test
    public void loadSessionFactory() {
        assertThat(sessionFactory).isNotNull();
        Session session = sessionFactory.openSession();
        assertThat(session).isNotNull();
        assertTrue(session.isConnected());
        session.close();
    }

    @Test
    public void entitiesScanned() {
        Session session = sessionFactory.openSession();
        Set<EntityType<?>> entities = session.getEntityManagerFactory().getMetamodel().getEntities();
        assertThat(entities.size()).isGreaterThanOrEqualTo(8);
    }
}
