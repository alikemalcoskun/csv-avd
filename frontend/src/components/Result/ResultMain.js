import { Table, Typography } from 'antd';
import ReactECharts from 'echarts-for-react';

export const ResultMain = ({ result }) => {
    if (!result) {
        return null;
    }

    if (result.type === 'data_analyze') {
        return (
            <Typography.Text>{result.main}</Typography.Text>
        );
    } else if (result.type === 'data_tabulate') {
        const data = JSON.parse(result.main);
        const columns = data.metadata.columns.map((column, index) => ({
            title: column,
            dataIndex: column,
            key: index.toString()
        }));

        const dataSource = data.data.map((row, index) => {
            return {
                key: index,
                ...row[index]
            };
        });

        return (
            <Table columns={columns} dataSource={dataSource} />
        );
    } else if (result.type === 'data_visualize') {
        const data = JSON.parse(result.main);
        const option = {
            title: {
                text: data.metadata.title
            },
            tooltip: {},
            xAxis: {
                data: data.data.map(d => d.name)
            },
            yAxis: {},
            series: [{
                name: data.metadata.y_axis,
                type: data.type,
                data: data.data.map(d => d.value)
            }]
        };

        return (
            <ReactECharts option={option} />
        );
    } else if (result.type === 'data_machine_learning') {
        return (
            <Typography.Text>{result.main}</Typography.Text>
        );
    } else {
        return null;
    }
}