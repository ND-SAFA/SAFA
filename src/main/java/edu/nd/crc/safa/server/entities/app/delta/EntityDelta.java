package edu.nd.crc.safa.server.entities.app.delta;

import java.util.Hashtable;

import org.json.JSONObject;

/**
 * Contains the entity changes that can occur between two projects versions.
 */
public class EntityDelta<BaseEntity> {
    Hashtable<String, BaseEntity> added;
    Hashtable<String, ModifiedEntity<BaseEntity>> modified;
    Hashtable<String, BaseEntity> removed;

    public EntityDelta() {
    }

    public EntityDelta(Hashtable<String, BaseEntity> added,
                       Hashtable<String, ModifiedEntity<BaseEntity>> modified,
                       Hashtable<String, BaseEntity> removed) {
        this.added = added;
        this.modified = modified;
        this.removed = removed;
    }

    public Hashtable<String, BaseEntity> getAdded() {
        return this.added;
    }

    public void setAdded(Hashtable<String, BaseEntity> added) {
        this.added = added;
    }

    public Hashtable<String, ModifiedEntity<BaseEntity>> getModified() {
        return this.modified;
    }

    public void setModified(Hashtable<String, ModifiedEntity<BaseEntity>> modified) {
        this.modified = modified;
    }

    public Hashtable<String, BaseEntity> getRemoved() {
        return this.removed;
    }

    public void setRemoved(Hashtable<String, BaseEntity> removed) {
        this.removed = removed;
    }

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("added", this.added);
        json.put("removed", this.removed);
        json.put("modified", this.modified);
        return json.toString();
    }
}
