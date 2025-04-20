import * as authActions from "../actions/auth.actions";

import { createReducer, on } from "@ngrx/store";

import { getAuthInitState } from "../auth.state";

export const authReducer = createReducer(
    getAuthInitState(),
    on(authActions.setCurrentUser, (state, action) => ({
        ...state,
        user: action.user
    })),
    on(authActions.setAccessToken, (state, action) => ({
        ...state,
        accessToken: action.token
    })),
    on(authActions.setEmailVerified, (state, action) => ({
        ...state,
        emailVerified: action.emailVerified
    })),
);