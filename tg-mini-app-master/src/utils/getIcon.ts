export const getIconPath = (iconHash: string) => {
  return `${import.meta.env.VITE_BUCKET_URL}/aenolabsfiles/${iconHash}`;
};
