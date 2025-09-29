// src/components/QuestionsList.js
'use client';
import styles from './Questionlist.module.css'; // <-- 1. IMPORT THE CSS MODULE

export default function QuestionsList({ data }) {
  if (!data || data.length === 0) {
    return <p>No data to display.</p>;
  }

  const questions = data.filter(comment => comment.is_question === true);

  if (questions.length === 0) {
    return <p>No questions were found in the comments.</p>;
  }

  // 2. APPLY THE NEW STYLES
  return (
    <div className={styles.listContainer}>
      <h3 className={styles.listTitle}>Questions Found in Comments</h3>
      <ul className={styles.questionList}>
        {questions.map(q => (
          <li key={q.id} className={styles.questionCard}>
            <p>{q.comment_text}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}