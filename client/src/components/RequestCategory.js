import React, { Component } from 'react';
import { Row } from 'react-bootstrap';
import { itemTypesByCategory, itemInfo } from '../constants';
import CategoryNav from './CategoryNav';
import Tile from './Tile';
import { Link } from 'react-router-dom';


class RequestItem extends Component {

  constructor(props) {
      super(props);
      this.state = {
          form: false,
          category: ''
      };

      this.formToggle = this.formToggle.bind(this);
  }

  formToggle(event, category) {
      this.context.router.push('/' + category);
      /*console.log(category);

      this.setState(({ form }) => {
          console.log(!form);
          return { form: !form, category: category }
      });*/
  }


  render() {
    const { displayName, icon } = this.props.info;
    const name = this.props.name;
    const category = this.props.category;

    // TODO: Put these styles in CSS/SASS
    return (
      <div className="col-sm-4 col-xs-12" style={{
        minWidth: '150px',
        minHeight: '150px',
      }}>
        <Link to={category + '/' + name}>
            <div>
                <Tile side='request' alt={displayName} icon={icon} />
                <h1 className="text-center tile-label">#NEEDED</h1>
                <p className='text-label'>{displayName}</p>
            </div>
        </Link>

      </div>
    )
  }
}


class RequestItemsLinks extends Component {
  render() {
    const { category } = this.props;

    const categoryItems = itemTypesByCategory[category];

    return (
      <Row>
        {
          categoryItems.map((item) => {
            return (<RequestItem key={ item } info={ itemInfo[item] } name={ item } category={ category }/>)
          })
        }
      </Row>
    )
  }
}


export default class RequestItemsList extends Component {
  render() {
    const { paths } = this.props;

    return (
      <div>
        <Row className='text-center'>
          <h2>
            Choose an item you need
          </h2>
        </Row>
        <Row>
          <CategoryNav paths={ paths } />
          <RequestItemsLinks { ...this.props } />
        </Row>
      </div>
    )
  }
}
