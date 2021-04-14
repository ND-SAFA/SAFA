package edu.nd.crc.safa.dao;

import java.util.Map;

import edu.nd.crc.safa.dao.Position;

/*
Position
{ 'x': 123, 'y': 432}

Layout
{ 'id': 'UAV-Root', 'positions': Map<String, Position> }
*/

public class Layout {
    public String id;
    public Map<String, Position> positions;
}