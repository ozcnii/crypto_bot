import styles from './thirdStory.module.css';

interface ThirdStoryProps {
  nextStory: () => void;
  currentIndex: number;
  storiesComponentsLength: number;
}

export const ThirdStory = ({
  nextStory,
  currentIndex,
  storiesComponentsLength,
}: ThirdStoryProps) => {
  return (
    <div className={styles.container}>
      <img
        src="img/backgrounds/stories3.jpg"
        alt="stories"
        height={'100%'}
        width={'100%'}
      />
      <div className={styles.buttonContainer}>
        <button onClick={nextStory} className={styles.nextButton}>
          {currentIndex < storiesComponentsLength - 1 ? 'Next' : 'Start'}
        </button>
      </div>
    </div>
  );
};
