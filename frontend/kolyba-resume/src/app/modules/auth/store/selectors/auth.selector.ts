import { createFeatureSelector, createSelector } from "@ngrx/store";

import { AuthState } from "../auth.state";

export const selectAuthFeature = createFeatureSelector<AuthState>('auth');

export const selectUser = createSelector(
    selectAuthFeature,
    state => state.user
);

export const selectAccessToken = createSelector(
    selectAuthFeature,
    state => state.accessToken
);

export const selectEmailVerified = createSelector(
    selectAuthFeature,
    state => state.emailVerified
);

export const selectHasResume = createSelector(
    selectUser,
    user => user?.hasResume
);