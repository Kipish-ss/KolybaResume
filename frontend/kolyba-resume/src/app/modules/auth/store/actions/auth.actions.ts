import { createAction, props } from '@ngrx/store';

import { NewUser } from '@auth//models/new-user';
import { User } from '@auth//models/user';

export const signIn = createAction('[Auth] Sign In', props<{ email: string; password: string }>());

export const signUp = createAction('[Auth] Sign Up', props<{ email: string; password: string; userName: string }>());

export const createUser = createAction('[Auth] Create User', props<{ user: NewUser }>())
export const createUseruccess = createAction('[Auth] Create User Success', props<{ user: User }>());
export const createUserFailure = createAction('[Auth] Create User Failure', props<{ error: Error }>());

export const resetPassword = createAction('[Auth] Reset Password', props<{ email: string }>());
export const resetPasswordSuccess = createAction('[Auth] Reset Password Success');
export const resetPasswordFailure = createAction('[Auth] Reset Password Failure', props<{ error: Error }>());

export const signOut = createAction('[Auth] Sign Out');
export const signOutSuccess = createAction('[Auth] Sign Out Success');
export const signOutFailure = createAction('[Auth] Sign Out Failure', props<{ error: Error }>());

export const sendVerificationEmail = createAction('[Auth] Send verification email');

export const refreshToken = createAction('[Auth] Refresh token');
export const setAccessToken = createAction('[Auth] Set Access Token', props<{ token: string }>());
export const setEmailVerified = createAction('[Auth] Set Email Verified', props<{ emailVerified: boolean }>());

export const loadCurrentUser = createAction('[Auth] Load Current User');
export const setCurrentUser = createAction('[Auth] Set Current User', props<{ user: User }>());
export const loadCurrentFailure = createAction('[Auth] Load Current User Failure', props<{ error: Error }>());

export const uploadResume = createAction('[Auth] Upload Resume', props<{ resume: File }>());
export const uploadResumeSuccess = createAction('[Auth] Upload Resume Success');
export const uploadResumeFailure = createAction('[Auth] Upload Resume Failure', props<{ error: Error }>());