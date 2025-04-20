import * as authActions from '../actions/auth.actions';
import * as authSelectors from '../selectors/auth.selector';

import { Injectable, inject } from '@angular/core';

import { Store } from '@ngrx/store';
import { User } from '@auth//models/user';

@Injectable({ providedIn: 'root' })
export class AuthStoreService {
    public user$ = this.store.select(authSelectors.selectUser);
    public accessToken$ = this.store.select(authSelectors.selectAccessToken);
    public emailVerified$ = this.store.select(authSelectors.selectEmailVerified);

    public constructor(private readonly store: Store) { }

    public signUp(email: string, password: string, userName: string): void {
        this.store.dispatch(authActions.signUp({ email, password, userName }));
    }

    public signIn(email: string, password: string): void {
        this.store.dispatch(authActions.signIn({ email, password }));
    }

    public setUser(user: User): void {
        this.store.dispatch(authActions.setCurrentUser({ user }));
    }

    public setAccessToken(token: string): void {
        this.store.dispatch(authActions.setAccessToken({ token }));
    }

    public setEmailVerified(emailVerified: boolean): void {
        this.store.dispatch(authActions.setEmailVerified({ emailVerified }));
    }
}
