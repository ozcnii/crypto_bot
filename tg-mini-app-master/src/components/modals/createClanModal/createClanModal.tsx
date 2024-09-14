import { RootState } from '@/store';
import { createClan } from '@/store/clanSlice';
import { ThunkDispatch } from '@reduxjs/toolkit';
import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router';
import css from './createClanModal.module.css';

const validateLink = (link: string) => {
  const pattern = /^t\.me\/[a-zA-Z0-9_]{5,}$/;
  return pattern.test(link);
};

export const CreateClanModal = () => {
  const dispatch = useDispatch<ThunkDispatch<RootState, null, any>>();
  const navigate = useNavigate();
  const [link, setLink] = useState<string>('t.me/');
  const [error, setError] = useState<string>('');

  const handleCreateClan = async () => {
    if (!validateLink(link)) {
      setError('Please enter a link in the format t.me/username.');
      return;
    }
    setError(''); // Clear error if link is valid

    const data = await dispatch(createClan(link));
    if (createClan.fulfilled.match(data)) {
      const { id } = data.payload;
      setLink('');
      navigate(`/clans/${id}`);
    } else {
      console.log(data);
    }
  };

  return (
    <div className={css.modal}>
      <div className={css.modalImgContainer}>
        <img src="img/modal.svg" alt="modal" className={css.modalImg} />
        <img
          src="img/playground.png"
          alt="modal"
          className={css.modalPlayGround}
        />
      </div>
      <div className={css.modalText}>
        <h1>Create a Clan</h1>
        <p>
          Lorem ipsum dolor sit amet consectetur. Elementum lorem massa
          consectetur id scelerisque in egestas amet rhoncus.
        </p>
      </div>
      <div className={css.inputModal}>
        <h1>Telegram Handle</h1>
        <div className={css.inputWrapper}>
          <div className={css.inputLogo}>
            <img src="img/safety-pin.png" alt="safety-pin" />
          </div>
          <input
            type="text"
            placeholder="t.me/username"
            value={link}
            onChange={(e) => setLink(e.target.value)}
            className={css.input}
          />
          <button
            className={css.arrowRight}
            type="button"
            onClick={handleCreateClan}
          >
            <img src="img/arrowRight.svg" alt="arrowRight" />
          </button>
        </div>
        {error && <p className={css.error}>{error}</p>}
        <p>Channel or Chat where you are an owner</p>
      </div>
      <div className={css.createClanContainer}>
        <div className={css.attention}>
          <div className={css.logo}>
            <img src="img/sparkles.png" alt="sparkles" />
          </div>
          <p>
            Before creating a Clan you need to add this bot @aenolabsbot to you
            channel or group as an admin. You can delete it after successful
            verification.
          </p>
        </div>
        <button
          className={css.createClan}
          onClick={handleCreateClan}
          type="button"
        >
          Create
        </button>
      </div>
    </div>
  );
};
