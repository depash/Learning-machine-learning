'use client';
import styles from './recommendationsComponent.module.css';

export const RecommendationsComponent = () => {
    const handleButtonClick = async () => {
        try {
            fetch('http://localhost:5000/recommend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ liked: ["Inception", "The Matrix"] })
            })
                .then(res => res.json())
                .then(data => console.log(data));
        } catch (error) {
            console.error("Error fetching recommendations:", error);
        }
    };

    return (
        <div className={styles.page}>
            <button className={styles.button} onClick={handleButtonClick}>
                Get Recommendations
            </button>
        </div>
    );
}