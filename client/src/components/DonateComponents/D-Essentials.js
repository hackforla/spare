import React, { Component } from 'react';
import Tile from '../Tile.js';
import { Grid, Row, Col } from 'react-bootstrap';
import { ITEMS } from '../../constants/CONSTANTS';

export default class Essentials extends Component {
    state = {}
    render() {
        var row = [];
        var rows = ITEMS.essentials.reduce((accum, item, index, array) => {
            row.push(
                <Col sm={3} key={item.index}>
                    <Tile item={item} request={'donate'}/>
                    <p className='text-label-small'>{item.name}</p>
                </Col>
            );
            if (!(row.length % 4) || index === array.length-1) {
                accum.push(<Row className="show-grid" key={index}>{row}</Row>);
                row = [];
            };
            return accum;
        }, []);
      
        return (<div>
            <h2>Essentials</h2>
            <Grid>
                { rows }
            </Grid>
        </div>)
    }
};
