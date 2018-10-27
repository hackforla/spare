import React, { Component, Fragment } from 'react';
import { Link } from 'react-router-dom';
import ReactSVG from 'react-svg'

class Tile extends Component {
  /* props:
   * icon (path to .png file)
   * side ('request' or 'donate'?)
   * alt (name for alt text field of image)
   */

  render() {
    const {
      category,
      disabled,
      displayName,
      side,
      subcategory,
      icon,
      hoverText
    } = this.props;

    //<Link to={ '/donate/' + category + '/' + subcategory + '/' } >
    const href = `/${side}/${category}/${subcategory}/`;

    // If production environment, prefix asset URL with `/static`
    // TODO: Find a better way to do this (PUBLIC_URL doesn't quite fit our use case)
    const src = `${process.env.NODE_ENV === 'production' ? '/static' : ''}/assets/tiles/${side}/${icon}`;

    let hover = null;
    if (!disabled && hoverText) {
      if (hoverText) hover = <div className="tile-hover-text">{ hoverText }</div>;
    }

    let content = (
      <Fragment>
        <div className='tile'>
          <ReactSVG alt={displayName} src={src} />
          { hover }
        </div>
        {!disabled && <div className='text-label'>{ displayName }</div>}
      </Fragment>
    );
    if (!disabled) {
      content = <Link to={ href }>{ content }</Link>;
    }

    return <div className="tile-container">{ content }</div>;
  }
}

export default Tile;
