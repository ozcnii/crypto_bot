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
            order.status !== 'open' &&
            order.contract_pair === action.payload.contract_pair,
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
