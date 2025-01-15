import { LoadingStatus } from '@/constants';

export type User = {
  balance: number;
  balance_features: number;
  boosters: number[];
  chat_id: number;
  clan?: number | null;
  historycheck: any;
  league: string;
  pnl: any;
  referals: any;
  tasks: any;
  trades: any;
  username: string;
};

export type AllUsers = {
  user: User;
  status: LoadingStatus;
  error: LoadingStatus;
};

export type UserResponse = {
  user: AllUsers;
};
