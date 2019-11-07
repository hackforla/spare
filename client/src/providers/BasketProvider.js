import React, { Component } from 'react';

const BasketContext = React.createContext('basket');

class BasketProvider extends Component {
  state = {
    items: {}
  };

  addToBasket = (slug, quantity) => {
    const items = this.state.items;
    const prevQuantity = this.state.items[slug] || 0;

    let updatedQuantity = quantity;

    if (prevQuantity) {
      updatedQuantity = prevQuantity + quantity;
    }

    items[slug] = updatedQuantity;

    this.setState({ items });
  };

  removeFromBasket = (slug, quantity) => {
    const items = this.state.items;
    const prevQuantity = this.state.items[slug] || 0;

    let updatedQuantity = quantity;

    if (prevQuantity) {
      updatedQuantity = prevQuantity - quantity;
    }

    items[slug] = updatedQuantity;

    this.setState({ items });
  };

  render() {
    const value = {
      basket: this.state.items,
      addToBasket: this.addToBasket,
      removeFromBasket: this.removeFromBasket
    };

    return (
      <BasketContext.Provider value={ value }>
        { this.props.children }
      </BasketContext.Provider>
    )
  }
};


const BasketConsumer = BasketContext.Consumer;

export { BasketProvider, BasketConsumer };
