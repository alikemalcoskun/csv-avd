import { Space, Typography, Divider } from 'antd';
import { ResultMain } from './ResultMain';

export const Result = ({ result }) => {
    return (
        <Space direction="vertical">
            <Divider orientation="left"
                style={{ borderColor: 'black', borderWidth: 2 }}
            >Result</Divider>
            <Typography.Text>{result.introduction}</Typography.Text>
            <ResultMain result={result} />
            <Typography.Text>{result.conclusion}</Typography.Text>
        </Space>
    );
}