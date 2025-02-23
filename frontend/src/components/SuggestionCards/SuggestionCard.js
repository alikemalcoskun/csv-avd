import {Card} from 'antd';

export const SuggestionCard = ({ icon, title, description, onClick }) => {
    return (
        <Card
        hoverable
        onClick={onClick}
        >
        <Card.Meta title={
            <>
            {icon}
            <span style={{ marginLeft: 10 }}>{title}</span>
            </>
        } description={description} />
        </Card>
    );
}