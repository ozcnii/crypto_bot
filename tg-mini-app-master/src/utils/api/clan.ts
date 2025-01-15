import axios from '@/utils/axios';
import { Clan } from '@/utils/types/clan';

export const getUserClanRequest = async (
  clanId: number | undefined,
): Promise<Clan | null> => {
  if (!clanId) {
    return null;
  }

  const resp = await axios.get(`/clans/get/${clanId}`);
  if (resp.status === 404) {
    return null; // Возвращаем null если 404 ошибка
  } else {
    const response = await axios.get(`/clans`);
    return {
      ...resp.data,
      usersList: response.data,
    };
  }
};

export const deleteUserClanRequest = async (link: string) => {
  return await axios.delete(`/users/clan/delete?client_id=1`, {
    data: link,
  });
};

export const joinUserClanRequest = async (id: number) => {
  return await axios.post(`/users/clan/join?client_id=1`, id);
};

export const leaveUserClanRequest = async () => {
  return await axios.get(`/users/clan/leave?client_id=1`);
};

export const getClanListRequest = async () => {
  const resp = await axios.get(`/clans/list?client_id=1`);

  return resp.data;
};

export const getClanByIdRequest = async (clanId: string | undefined) => {
  const resp = await axios.get(`/clans/get/${clanId}`);
  return resp.data;
};

export const createClanRequest = async (link: string) => {
  const resp = await axios.post(`/users/clan/create?client_id=1`, link);
  return resp;
};
