import React, { Component } from 'react';

class Tile extends Component {
    /* props:
     * item (json object from CONSTANTS)
     * amount (number of items currently requested)
     */

    render() {
        var src = `assets/tiles/${this.props.request}/${this.props.item.ref}`;
        return (
            <div className='tile'>
                <img alt={this.props.item.name.toLowerCase()} src={src} />
            </div>
        )
    }
}

export default Tile;

                
                
