import 'swiper/css';
import { FreeMode } from 'swiper/modules';
import { Swiper, SwiperSlide } from 'swiper/react';
import { BoosterSwiperCard } from './boosterSwiperCard';
import css from './boostersSwiper.module.css';

export const items = [
  {
    id: 1,
    img: '🪙',
    name: 'Range',
  },
  {
    id: 2,
    img: '⚖️',
    name: 'Leverage',
  },
  {
    id: 3,
    img: '⚡',
    name: 'Trades',
  },
  {
    id: 4,
    img: '🤖',
    name: 'Trading Bot',
  },
];

export const BoostersSwiper = () => {
  return (
    <Swiper
      spaceBetween={12.5}
      slidesPerView={'auto'}
      direction="vertical"
      modules={[FreeMode]}
      className={css.swiper}
    >
      {items.map((item) => (
        <SwiperSlide key={item.id} className={css.swiperSlide}>
          <BoosterSwiperCard item={item} />
        </SwiperSlide>
      ))}
    </Swiper>
  );
};
