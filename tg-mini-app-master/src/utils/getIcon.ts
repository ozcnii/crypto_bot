import { BUCKET_URL } from './constants';

export const getIconPath = (iconHash: string) => {
  return `${BUCKET_URL}/aenolabsfiles/${iconHash}`;
};
