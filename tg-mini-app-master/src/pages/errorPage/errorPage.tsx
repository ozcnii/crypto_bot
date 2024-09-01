import { FC } from 'react';
import css from './errorPage.module.css';

type ErrorPageProps = {
  error: string;
  code: number;
};

export const ErrorPage: FC<ErrorPageProps> = ({ error, code }) => {
  return (
    <div className={css.container}>
      <h1>{code}</h1>
      <p>{error}</p>
    </div>
  );
};
