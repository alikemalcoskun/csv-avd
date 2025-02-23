import { Upload, message, Button } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import * as XLSX from 'xlsx';
import * as Papa from 'papaparse';

export const FileUploadButton = ({ onFileSelect, filename, setFilename, setFileData }) => {
    const [messageApi, contextHolder] = message.useMessage();

    const convertXlsxToCsv = (buffer) => {
        const workbook = XLSX.read(buffer, { type: 'array' });
        const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
        return XLSX.utils.sheet_to_csv(firstSheet);
    };

    const handleFile = (file) => {
        const reader = new FileReader();
        
        reader.onload = (e) => {
            try {
                let csvContent;
                if (file.name.endsWith('.xlsx')) {
                    // Convert XLSX to CSV
                    const buffer = new Uint8Array(e.target.result);
                    csvContent = convertXlsxToCsv(buffer);
                } else {
                    // Direct CSV content
                    csvContent = e.target.result;
                }
                // Convert CSV to JSON
                const jsonContent = Papa.parse(csvContent, { header: true, skipEmptyLines: true }).data;
                
                // JSON to String
                const jsonString = JSON.stringify(jsonContent);

                setFileData(jsonString);
                setFilename(file.name);
            } catch (error) {
                messageApi.error('Error processing file: ' + error.message);
                console.error(error);
            }
        };

        if (file.name.endsWith('.xlsx')) {
            reader.readAsArrayBuffer(file);
        } else {
            reader.readAsText(file);
        }
    };

    const props = {
        beforeUpload: (file) => {
            const isCsv = file.type === 'text/csv' || file.name.endsWith('.csv');
            const isXlsx = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || file.name.endsWith('.xlsx');
            
            if (!isCsv && !isXlsx) {
                messageApi.open({
                    type: 'error',
                    content: 'You can only upload CSV or XLSX files!',
                });
                return Upload.LIST_IGNORE;
            }
            
            handleFile(file);
            onFileSelect(file);
            return false;
        },
        maxCount: 1,
    };

    return (
        <>
            {contextHolder}
            <Upload {...props} showUploadList={false}>
                <Button icon={<UploadOutlined />} size="large">
                    {filename ? filename : 'Click to upload'}
                </Button>
            </Upload>
        </>
    );
};
