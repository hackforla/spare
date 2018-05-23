import React, { Component } from 'react';

class Tile extends Component {
  /* props:
   * icon (path to .png file)
   * side ('request' or 'donate'?)
   * alt (name for alt text field of image)
   */

  render() {
    var src = `/assets/tiles/${this.props.side}/${this.props.icon}`;
    return (
      <div className='tile' onClick={this.props.onClick}>
        <img alt={this.props.alt} src={src} />
        { this.children }
      </div>
    )
  }
}

export default Tile;
