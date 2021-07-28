package unit.entities;

import org.hibernate.Session;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import unit.SpringBootBaseTest;

public class EntityBaseTest extends SpringBootBaseTest {
    Session session;

    @BeforeEach
    public void loadSession() {
        session = this.sessionFactory.openSession();
    }

    @AfterEach
    public void closeSession() {
        if (session != null) {
            session.close();
        }
    }
}
