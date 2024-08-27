export interface Order {
  id: number;
  user_id: number;
  contract_pair: string;
  entry_rate: number;
  exit_rate?: number;
  amount: number;
  direction: string;
  status: string; // 'open', 'closed', 'pending'
  created_at: string;
  closed_at?: string;
  leverage?: number;
}

export interface OrdersState {
  orders: Order[];
  currentOrder: Order | null;
  loading: boolean;
  error: string | null;
}

export interface OrderCreatePayload {
  contract_pair: string;
  direction: string;
  amount: number;
  leverage?: number;
}

export interface OrderClosePayload {
  id: number;
}
