import styles from './secondStory.module.css';

interface SecondStoryProps {
  nextStory: () => void;
  currentIndex: number;
  storiesComponentsLength: number;
}

export const SecondStory = ({
  nextStory,
  currentIndex,
  storiesComponentsLength,
}: SecondStoryProps) => {
  return (
    <div className={styles.container}>
      <img
        src="img/backgrounds/stories2.jpg"
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
