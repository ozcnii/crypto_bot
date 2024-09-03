import { closeModal } from '@/store/modalsSlice';
import axios from '@/utils/axios';
import { Order, OrderCreatePayload, OrdersState } from '@/utils/types/orders';
import { createAsyncThunk, createSlice, PayloadAction } from '@reduxjs/toolkit';

export const createOrder = createAsyncThunk(
  'orders/createOrder',
  async (orderData: OrderCreatePayload, { rejectWithValue }) => {
    try {
      const response = await axios.post(
        '/orders/create?client_id=1',
        orderData,
      );
      return response.data; // Это будет передано в экшен fulfilled
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  },
);

export const closeOrder = createAsyncThunk(
  'orders/closeOrder',
  async (orderDataId: number, { rejectWithValue }) => {
    try {
      const response = await axios.post(
        `/orders/close/${orderDataId}?client_id=1`,
      );
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  },
);

export const getOrders = createAsyncThunk(
  'orders/getOrders',
  async ({ contract_pair }: { contract_pair: string }, { rejectWithValue }) => {
    try {
      const response = await axios.get('/orders/list?client_id=1');
      return {
        orders: response.data,
        contract_pair,
      };
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  },
);

export const getCurrentOrder = createAsyncThunk(
  'orders/getCurrentOrder',
  async (
    { contract_address }: { contract_address: string },
    { rejectWithValue },
  ) => {
    try {
      const response = await axios.get(
        `/orders/current/${contract_address}?client_id=1`,
      );
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  },
);

export const getClosedOrders = createAsyncThunk(
  'orders/getClosedOrders',
  async (_, { rejectWithValue }) => {
    try {
      const response = await axios.get('/orders/closed?client_id=1');
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  },
);

const pairs = {
  'EQARK5MKz_MK51U5AZjK3hxhLg1SmQG2Z-4Pb7Zapi_xwmrN': 'NOTUSDT',
  'EQA-X_yo3fzzbDbJ_0bzFWKqtRuZFIRa1sJsveZJ1YpViO3r': 'TONUSDT',
  '0xc7bbec68d12a0d1830360f8ec58fa599ba1b0e9b': 'ETHUSDT',
  '0xa43fe16908251ee70ef74718545e4fe6c5ccec9f': 'PEPEUSDT',
  '0x6aa9c4eda3bf8ac038ad5c243133d6d25aa9cc73': 'BTCUSDT',
  DSUvc5qf5LJHHV5e2tD184ixotSnCnwj7i4jJa4Xsrmt: 'SOLUSDT',
};

const initialState: OrdersState = {
  orders: [],
  currentOrder: null,
  loading: false,
  error: null,
};

const ordersSlice = createSlice({
  name: 'orders',
  initialState,
  reducers: {
    clearOrders: (state) => {
      state.orders = [];
    },
    clearCurrentOrder: (state) => {
      state.currentOrder = null;
    },
  },
  extraReducers: (builder) => {
    // Очистка стейта после закрытия модального окна
    builder.addCase(closeModal, (state) => {
      state.currentOrder = null;
      state.orders = [];
      state.loading = false;
      state.error = null;
    });
    // Обработка создания ордера
    builder.addCase(createOrder.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(
      createOrder.fulfilled,
      (state, action: PayloadAction<Order>) => {
        state.loading = false;
        state.orders.push(action.payload);
      },
    );
    builder.addCase(createOrder.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload as string;
    });

    // Обработка закрытия ордера
    builder.addCase(closeOrder.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(
      closeOrder.fulfilled,
      (state, action: PayloadAction<Order>) => {
        state.loading = false;
        const index = state.orders.findIndex(
          (order) => order.id === action.payload.id,
        );
        if (index !== -1) {
          state.orders[index] = action.payload;
        }
      },
    );
    builder.addCase(closeOrder.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload as string;
    });

    // Обработка получения ордеров
    builder.addCase(getOrders.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(
      getOrders.fulfilled,
      (
        state,
        action: PayloadAction<{ orders: Order[]; contract_pair: string }>,
      ) => {
        state.loading = false;
        state.orders = action.payload.orders.filter(
          (order) =>
            order.status === 'closed' &&
            order.contract_pair === pairs[action.payload.contract_pair],
        );
      },
    );
    builder.addCase(getOrders.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload as string;
    });

    // Обработка получения текущего ордера
    builder.addCase(getCurrentOrder.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(
      getCurrentOrder.fulfilled,
      (state, action: PayloadAction<Order | null>) => {
        state.loading = false;
        state.currentOrder = action.payload;
      },
    );
    builder.addCase(getCurrentOrder.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload as string;
    });
  },
});

export const { clearOrders, clearCurrentOrder } = ordersSlice.actions;

export default ordersSlice.reducer;
