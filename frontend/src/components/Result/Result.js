import { Space, Typography } from 'antd';
import { ResultMain } from './ResultMain';

export const Result = ({ result }) => {
    return (
        <Space direction="vertical">
            <Typography.Title level={4}>Result</Typography.Title>
            <Typography.Text>{result.introduction}</Typography.Text>
            <ResultMain result={result} />
            <Typography.Text>{result.conclusion}</Typography.Text>
        </Space>
    );
}