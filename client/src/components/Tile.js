import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Tile extends Component {
  /* props:
   * icon (path to .png file)
   * side ('request' or 'donate'?)
   * alt (name for alt text field of image)
   */

  render() {
    const {
      category,
      displayName,
      side,
      subcategory,
      icon,
      hoverText
    } = this.props;

    //<Link to={ '/donate/' + category + '/' + subcategory + '/' } >
    const href = `/${side}/${category}/${subcategory}/`;
    const src = `/assets/tiles/${side}/${icon}`;

    const hover = hoverText ? (
      <div className="tile-hover-text">{ hoverText }</div>
    ) : null

    return (
      <div className="tile-container">
        <Link to={ href }>
          <div className='tile'>
            <img alt={displayName} src={src} />
            { hover }
          </div>
          <div className='text-label'>{ displayName }</div>
        </Link>
      </div>
    )
  }
}

export default Tile;
