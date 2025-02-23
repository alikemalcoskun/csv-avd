import { Modal } from 'antd';

export const APIKeyModal = ({ visible, onOk, onCancel }) => {
    return (
        <Modal
            title="API Key Required"
            open={visible}
            onOk={onOk}
            onCancel={onCancel}
            closable={false}
            maskClosable={false}
            okButtonProps={{ disabled: true }}
            cancelButtonProps={{ disabled: true }}
        >
            <p>WARNING: You need an OpenAI API key to use this service. Please check the README file for more information.</p>
        </Modal>
    );
};
