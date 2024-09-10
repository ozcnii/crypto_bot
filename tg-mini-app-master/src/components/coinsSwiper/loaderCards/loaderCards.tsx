import { FreeMode, Scrollbar } from 'swiper/modules';
import { Swiper, SwiperSlide } from 'swiper/react';
import { EmptyCoinListItem } from './emptyCoinListItem/emptyCoinListItem';
import css from './styles.module.css';

export const LoaderCards = () => {
  return (
    <Swiper
      slidesPerView="auto"
      spaceBetween={15}
      modules={[FreeMode, Scrollbar]}
      scrollbar={{ draggable: true }}
      freeMode
      direction="vertical"
      className={css.swiper}
    >
      {Array.from({ length: 6 }).map((_, index) => (
        <SwiperSlide key={index} className={css.swiperSlide}>
          <EmptyCoinListItem />
        </SwiperSlide>
      ))}
    </Swiper>
  );
};
