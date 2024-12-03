import styles from './firstStory.module.css';

interface FirstStoryProps {
  nextStory: () => void;
  currentIndex: number;
  storiesComponentsLength: number;
}

export const FirstStory = ({
  nextStory,
  currentIndex,
  storiesComponentsLength,
}: FirstStoryProps) => {
  return (
    <div className={styles.container}>
      <img
        src="img/backgrounds/stories.jpg"
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
