import './App.css';
import { useState } from 'react';
import { Typography, Space, Input, Button, Layout, message } from 'antd';
import { SendOutlined, HighlightOutlined, TableOutlined, LineChartOutlined, PartitionOutlined, LoadingOutlined } from '@ant-design/icons';
import { SuggestionCards } from './components/SuggestionCards/SuggestionCards';
import { FileUploadButton } from './components/FileUploadButton/FileUploadButton';

// Axios
import axios from 'axios';

import { Result } from './components/Result/Result';

function App() {
  const [messageApi, contextHolder] = message.useMessage();

  const [inputText, setInputText] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [filename, setFilename] = useState('');
  const [fileData, setFileData] = useState(null);
  const [useDefaultData, setUseDefaultData] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileSelect = (file) => {
    setSelectedFile(file);
  };
  const handleFileData = (data) => {
    setFileData(data);
    setUseDefaultData(false);
  }

  const handleSend = () => {
    if (!inputText) {
      messageApi.error('Please type your question');
      return;
    }

    if (!selectedFile && !useDefaultData) {
      messageApi.error('Please select a file');
      return;
    }

    setLoading(true);
    messageApi.loading('Sending the request...');
    
    const data = useDefaultData ? '' : fileData;
    axios.post('http://localhost:5172/api/v1/agent/run', {
      user_question: inputText,
      data: data,
      use_default_data: useDefaultData
    })
      .then((response) => {
        console.log(response.data.result);
        setResult(response.data.result);
        messageApi.success('Request completed successfully');
      })
      .catch((error) => {
        if (error?.response?.data?.detail && typeof error.response.data.detail === 'string') {
          messageApi.error(error.response.data.detail);
        } else {
          messageApi.error('An error occurred while sending the request');
        }
        console.error(error);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const suggestions = [
    {
      icon: <HighlightOutlined />,
      title: 'Analyze',
      description: 'What is the transaction with the highest price?',
      onClick: () => {
        setInputText('What is the transaction with the highest price?')
        setFilename('Stock_Trading_History.csv');
        setUseDefaultData(true);
      }
    },
    {
      icon: <TableOutlined />,
      title: 'Tabulate',
      description: 'List 5 transactions with the highest price.',
      onClick: () => {
        setInputText('List 5 transactions with the highest price.')
        setFilename('Stock_Trading_History.csv');
        setUseDefaultData(true);
      }
    },
    {
      icon: <LineChartOutlined />,
      title: 'Visualize',
      description: 'Give me a chart about the quantities of automatic transactions.',
      onClick: () => {
        setInputText('Give me a chart about the quantities of automatic transactions.')
        setFilename('Stock_Trading_History.csv');
        setUseDefaultData(true);
      }
    },
    {
      icon: <PartitionOutlined />,
      title: 'Machine Learning',
      description: 'Predict the price of the next transaction based on the previous transactions.',
      onClick: () => {
        setInputText('Predict the price of the next transaction based on the previous transactions.')
        setFilename('Stock_Trading_History.csv');
        setUseDefaultData(true);
      }
    }
  ];

  return (
    <>
      {contextHolder}
      <Layout style={{ 
        minHeight: '100vh', 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center',
      }}>
        <Typography.Title level={2}>CSV Multi Agent</Typography.Title>
        <Typography.Text type="secondary">Choose your file and ask your question.</Typography.Text>
        <Space direction="vertical" size={12} style={{ width: '100%', maxWidth: '800px', padding: '20px 20px', alignItems: 'center' }}>
          <SuggestionCards suggestions={suggestions} maxCols={2} />
          <Space.Compact style={{ width: '100%' }}>
            <Input 
              placeholder="Type your question here..." 
              size="large"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)} 
              style={{
                minWidth: 600,
              }}
            />
  <FileUploadButton onFileSelect={handleFileSelect} filename={filename} setFilename={setFilename} setFileData={handleFileData} />
            <Button 
              type="primary" 
              size="large" 
              icon={((loading && <LoadingOutlined />) || <SendOutlined />)}
              disabled={loading}
              onClick={handleSend}
            >
              Send
            </Button>
          </Space.Compact>
        </Space>
        <div style={{ margin: 96 }}>
          {((result && <Result result={result} />))}
        </div>
      </Layout>
    </>
  );
}

export default App;
