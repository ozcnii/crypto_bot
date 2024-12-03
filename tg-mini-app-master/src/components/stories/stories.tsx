import { FC, useEffect, useState } from 'react';
import { FirstStory } from './firstStory/firstStory';
import { SecondStory } from './secondStory/secondStory';
import styles from './stories.module.css';
import { ThirdStory } from './thirdStory/thirdStory';

export const Stories: FC = () => {
  const [showStories, setShowStories] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);

  const nextStory = () => {
    if (currentIndex < storiesComponents.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      setShowStories(false);
    }
  };

  const storiesComponents = [
    <FirstStory
      nextStory={nextStory}
      currentIndex={currentIndex}
      storiesComponentsLength={3}
    />,
    <SecondStory
      nextStory={nextStory}
      currentIndex={currentIndex}
      storiesComponentsLength={3}
    />,
    <ThirdStory
      nextStory={nextStory}
      currentIndex={currentIndex}
      storiesComponentsLength={3}
    />,
  ];

  useEffect(() => {
    const showStories = localStorage.getItem('showStories');
    if (!showStories) {
      setShowStories(true);
      localStorage.setItem('showStories', 'true');
    }
  }, []);

  if (!showStories) return null;

  return (
    <div className={styles.overlay}>{storiesComponents[currentIndex]}</div>
  );
};
