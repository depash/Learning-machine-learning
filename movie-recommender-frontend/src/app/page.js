import { RecommendationsComponent } from "./components/recommendationsComponent";
import styles from "./page.module.css";

export default function Home() {

  return (
    <div className={styles.page}>
      <RecommendationsComponent />
    </div>
  );
}
