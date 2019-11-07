import React, { Component } from 'react';
import Modal from 'react-modal';

Modal.setAppElement('#root');

class RequestModal extends Component {
  render() {
    const { style, isOpen, onRequestClose } = this.props;

    return (
      <Modal
        style={ style }
        isOpen={ isOpen }
        onRequestClose={ onRequestClose }
        shouldCloseOnOverlayClick={ true }
        contentLabel={ 'Add an item' }
      >
      </Modal>
    );
  }
}


export default RequestModal;
