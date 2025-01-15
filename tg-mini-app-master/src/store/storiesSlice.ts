import { createSlice } from '@reduxjs/toolkit';

interface StoriesState {
  isOpen: boolean;
}

const initialState: StoriesState = {
  isOpen: false,
};

const storiesSlice = createSlice({
  name: 'stories',
  initialState,
  reducers: {
    openStories: (state) => {
      state.isOpen = true;
    },
    closeStories: (state) => {
      state.isOpen = false;
    },
  },
});

export const { closeStories, openStories } = storiesSlice.actions;

export default storiesSlice.reducer;
