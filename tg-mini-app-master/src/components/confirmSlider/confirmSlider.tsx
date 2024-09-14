import { RootState } from '@/store';
import { upgradeUserBoosterByType } from '@/store/boostersSlice';
import { confirmBoost } from '@/store/modalsSlice';
import { ThunkDispatch } from '@reduxjs/toolkit';
import { FC, useEffect, useRef, useState } from 'react';
import { useDispatch } from 'react-redux';
import css from './confirmSlider.module.css';

interface ConfirmSliderProps {
  type: string;
}

export const ConfirmSlider: FC<ConfirmSliderProps> = ({ type }) => {
  const dispatch = useDispatch<ThunkDispatch<RootState, unknown, any>>();
  const [isDragging, setIsDragging] = useState(false);
  const [position, setPosition] = useState(0);
  const sliderRef = useRef<HTMLDivElement>(null);
  const currentPosRef = useRef(0); // Текущая позиция ползунка

  const handleDragStart = () => {
    setIsDragging(true);
  };

  const handleMouseMove = (event: MouseEvent) => {
    if (!isDragging || !sliderRef.current) return;

    const rect = sliderRef.current.getBoundingClientRect();
    let newPos = event.clientX - rect.left - 22.5; // 22.5 - половина ширины ползунка

    if (newPos < 0) newPos = 0;
    if (newPos > rect.width - 45) newPos = rect.width - 45; // 45 - ширина ползунка
    setPosition(newPos);
    currentPosRef.current = newPos; // Обновляем currentPosRef
  };

  const handleTouchMove = (event: TouchEvent) => {
    if (!isDragging || !sliderRef.current) return;

    const rect = sliderRef.current.getBoundingClientRect();
    let newPos = event.touches[0].clientX - rect.left - 22.5; // 22.5 - половина ширины ползунка

    if (newPos < 0) newPos = 0;
    if (newPos > rect.width - 45) newPos = rect.width - 45; // 45 - ширина ползунка
    setPosition(newPos);
    currentPosRef.current = newPos; // Обновляем currentPosRef
  };

  const handleDragEnd = async () => {
    if (!sliderRef.current) return;

    const rect = sliderRef.current.getBoundingClientRect();
    const maxPosition = rect.width - 45; // 45 - ширина ползунка
    const finalPosition = currentPosRef.current; // Используем currentPosRef для получения позиции

    if (finalPosition >= maxPosition) {
      dispatch(confirmBoost(true));
      await dispatch(
        upgradeUserBoosterByType({
          booster_type: type,
        }),
      );
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

  // Рассчитываем ширину затемненной области
  const backgroundWidth = position;

  if (type === 'trading bot') {
    return (
      <div className={css.confirm_slider_container} ref={sliderRef}>
        <div className={css.slider_text}>
          Sorry, but that booster does not work yet
        </div>
      </div>
    );
  }

  return (
    <div className={css.confirm_slider_container} ref={sliderRef}>
      {/* Затемняющий фон за ползунком */}
      <div
        className={css.slider_background}
        style={{ width: `${backgroundWidth}px` }} // Ширина затемненной области
      />
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
