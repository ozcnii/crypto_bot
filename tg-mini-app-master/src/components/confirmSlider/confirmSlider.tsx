import { confirmBoost } from '@/store/modalsSlice'
import { FC, useEffect, useRef, useState } from 'react'
import { useDispatch } from 'react-redux'
import css from './confirmSlider.module.css'

export const ConfirmSlider: FC = () => {
  const dispatch = useDispatch();
  const [isDragging, setIsDragging] = useState(false);
  const [position, setPosition] = useState(0);
  const sliderRef = useRef<HTMLDivElement>(null);
  const currentPosRef = useRef(0); // Добавляем useRef для хранения текущей позиции

  const handleDragStart = () => {
    setIsDragging(true);
    console.log('Drag started');
  };

  const handleMouseMove = (event: MouseEvent) => {
    if (!isDragging || !sliderRef.current) return;
    
    const rect = sliderRef.current.getBoundingClientRect();
    let newPos = event.clientX - rect.left - 22.5; // 22.5 - половина ширины ползунка
    console.log('Mouse move: ', { eventClientX: event.clientX, rectLeft: rect.left, newPos });

    if (newPos < 0) newPos = 0;
    if (newPos > rect.width - 45) newPos = rect.width - 45; // 45 - ширина ползунка
    setPosition(newPos);
    currentPosRef.current = newPos; // Обновляем currentPosRef
  };

  const handleTouchMove = (event: TouchEvent) => {
    if (!isDragging || !sliderRef.current) return;
    
    const rect = sliderRef.current.getBoundingClientRect();
    let newPos = event.touches[0].clientX - rect.left - 22.5; // 22.5 - половина ширины ползунка
    console.log('Touch move: ', { eventClientX: event.touches[0].clientX, rectLeft: rect.left, newPos });

    if (newPos < 0) newPos = 0;
    if (newPos > rect.width - 45) newPos = rect.width - 45; // 45 - ширина ползунка
    setPosition(newPos);
    currentPosRef.current = newPos; // Обновляем currentPosRef
  };

  const handleDragEnd = () => {
    if (!sliderRef.current) return;

    const rect = sliderRef.current.getBoundingClientRect();
    const maxPosition = rect.width - 45; // 45 - ширина ползунка
    const finalPosition = currentPosRef.current; // Используем currentPosRef для получения позиции
    console.log('Drag end: ', { position: finalPosition, maxPosition });

    if (finalPosition >= maxPosition) {
      dispatch(confirmBoost(true));
    } else {
      dispatch(confirmBoost(false));
    }

    setPosition(0);
    setIsDragging(false);
  };

  useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleDragEnd);
      document.addEventListener('touchmove', handleTouchMove);
      document.addEventListener('touchend', handleDragEnd);
    } else {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleDragEnd);
      document.removeEventListener('touchmove', handleTouchMove);
      document.removeEventListener('touchend', handleDragEnd);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleDragEnd);
      document.removeEventListener('touchmove', handleTouchMove);
      document.removeEventListener('touchend', handleDragEnd);
    };
  }, [isDragging]);

  return (
    <div className={css.confirm_slider_container} ref={sliderRef}>
      <div className={css.slider_text}>Slide to confirm</div>
      <div
        className={css.slider_handle}
        style={{ transform: `translateX(${position}px)` }}
        onMouseDown={handleDragStart}
        onTouchStart={handleDragStart}
      >
        <div className={css.slider_arrow}>→</div>
      </div>
    </div>
  );
};