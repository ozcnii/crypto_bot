import axios from '@/utils/axios';
import { AxiosResponse } from 'axios';
import { Clan, ClanList } from '../types/clan';
import { User } from '../types/userType';

export const getUserByJWTRequest = async (
  userId: number,
): Promise<AxiosResponse<User>> => {
  const response = await axios.get(`/users/${userId}`);
  return response;
};

export const getUserClanRequest = async (): Promise<Clan> => {
  const response = await axios.post(`/users/current_user/clan?client_id=1`);
  return response.data;
};

export const getUserClanListRequest = async (): Promise<ClanList[]> => {
  const response = await axios.post(`/users/clan/list?client_id=1`);
  return response.data;
};
