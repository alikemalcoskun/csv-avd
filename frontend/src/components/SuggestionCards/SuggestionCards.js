import { SuggestionCard } from './SuggestionCard';
import { Row, Col } from 'antd';

export const SuggestionCards = ({ suggestions, maxCols = 2 }) => {
    const colSpan = 24 / maxCols;

    return (
        <Row gutter={[8, 16]}>
            {suggestions.map((suggestion, index) => (
                <Col 
                    key={index} 
                    xs={24}
                    sm={24}
                    md={colSpan}
                >
                    <SuggestionCard 
                        icon={suggestion.icon}
                        title={suggestion.title}
                        description={suggestion.description}
                        onClick={() => suggestion.onClick(suggestion.description)}
                    />
                </Col>
            ))}
        </Row>
    );
};
