import { FC, useEffect, useState } from 'react';
import { FirstStory } from './firstStory/firstStory';
import { SecondStory } from './secondStory/secondStory';
import styles from './stories.module.css';
import { ThirdStory } from './thirdStory/thirdStory';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '@/store';
import { closeStories, openStories } from '@/store/storiesSlice';

export const Stories: FC = () => {
  const dispatch = useDispatch();
  const { isOpen } = useSelector((state: RootState) => state.stories);
  const [currentIndex, setCurrentIndex] = useState(0);

  const nextStory = () => {
    if (currentIndex < storiesComponents.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      dispatch(closeStories());
      setCurrentIndex(0);
    }
  };

  const storiesComponents = [
    <FirstStory
      key={1}
      nextStory={nextStory}
      currentIndex={currentIndex}
      storiesComponentsLength={3}
    />,
    <SecondStory
      key={2}
      nextStory={nextStory}
      currentIndex={currentIndex}
      storiesComponentsLength={3}
    />,
    <ThirdStory
      key={3}
      nextStory={nextStory}
      currentIndex={currentIndex}
      storiesComponentsLength={3}
    />,
  ];

  useEffect(() => {
    const showStories = localStorage.getItem('showStories');
    if (!showStories) {
      dispatch(openStories());
      localStorage.setItem('showStories', 'true');
    }
  }, []);

  if (!isOpen) return null;

  return (
    <div className={styles.overlay}>{storiesComponents[currentIndex]}</div>
  );
};
