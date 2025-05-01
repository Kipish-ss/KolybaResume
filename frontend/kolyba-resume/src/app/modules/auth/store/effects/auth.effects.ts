import * as authActions from '../actions/auth.actions';

import { Actions, createEffect, ofType } from '@ngrx/effects';
import { Auth, createUserWithEmailAndPassword, sendEmailVerification, sendPasswordResetEmail, signInWithEmailAndPassword, signOut } from '@angular/fire/auth';
import { accessTokenLocalStorage, emailVerifiedLocalStorage, userLocalStorage } from '@core/constants/local-storage.constants';
import { catchError, from, map, mergeMap, of, switchMap, tap } from 'rxjs';

import { Injectable } from '@angular/core';
import { NotificationService } from '@core/services/notification.service';
import { Router } from '@angular/router';
import { SpinnerService } from '@core/services/spinner.service';
import { UserApiService } from '../services/user-api.service';

@Injectable()
export class AuthEffects {
    constructor(
        private actions$: Actions,
        private auth: Auth,
        private userApiService: UserApiService,
        private notificationService: NotificationService,
        private spinnerService: SpinnerService,
        private router: Router,
    ) { }

    public readonly signIn$ = createEffect(() =>
        this.actions$.pipe(
            ofType(authActions.signIn),
            tap(() => this.spinnerService.show()),
            switchMap(({ email, password }) =>
                from(signInWithEmailAndPassword(this.auth, email, password)).pipe(
                    switchMap(async (userCredential) => {
                        const token = await userCredential.user.getIdToken();
                        localStorage.setItem('accessToken', token);

                        if (!userCredential.user.emailVerified) {
                            return authActions.loadCurrentFailure({ error: new Error('email-not-verified') });
                        }

                        return authActions.loadCurrentUser();
                    }),
                ),
            ),
            tap(() => this.spinnerService.hide())
        )
    );

    public readonly loadCurrentUser$ = createEffect(() =>
        this.actions$.pipe(
            ofType(authActions.loadCurrentUser),
            switchMap(() => this.userApiService.getCurrentUser())
        )
    );

    public readonly loadCurrentUserSuccess$ = createEffect(() =>
        this.actions$.pipe(
            ofType(authActions.setCurrentUser),
            tap(() => this.router.navigateByUrl(''))
        ),
        { dispatch: false }
    );

    public readonly signUp$ = createEffect(() =>
        this.actions$.pipe(
            ofType(authActions.signUp),
            tap(() => this.spinnerService.show()),
            switchMap(({ email, password, userName }) => from(createUserWithEmailAndPassword(this.auth, email, password)).pipe(
                switchMap(userCredential => ([
                    authActions.sendVerificationEmail(),
                    authActions.createUser({
                        user: {
                            uid: userCredential.user?.uid,
                            userName: userCredential.user?.displayName ?? userName,
                            email: userCredential.user?.email ?? '',
                            image: userCredential.user?.photoURL ?? undefined,
                        }
                    })
                ]))
            )),
            tap(() => this.spinnerService.hide())
        ));

    public readonly setCurrentUser$ = createEffect(() =>
        this.actions$.pipe(
            ofType(authActions.setCurrentUser),
            tap(({ user }) => localStorage.setItem(userLocalStorage, JSON.stringify(user)))
        ),
        { dispatch: false }
    );

    public readonly setAccessToken$ = createEffect(() =>
        this.actions$.pipe(
            ofType(authActions.setAccessToken),
            tap(({ token }) => localStorage.setItem(accessTokenLocalStorage, token))
        ),
        { dispatch: false }
    );

    public readonly setEmailVerified$ = createEffect(() =>
        this.actions$.pipe(
            ofType(authActions.setEmailVerified),
            tap(({ emailVerified }) => localStorage.setItem(userLocalStorage, JSON.stringify(emailVerified)))
        ),
        { dispatch: false }
    );

    public readonly createUser$ = createEffect(() =>
        this.actions$.pipe(
            ofType(authActions.createUser),
            switchMap(({ user }) => this.userApiService.createUser(user))
        )
    );

    public readonly sendEmailVerification$ = createEffect(() =>
        this.actions$.pipe(
            ofType(authActions.sendVerificationEmail),
            tap(async () => {
                const user = this.auth.currentUser;
                if (user) {
                    await sendEmailVerification(user);
                }
            })
        ),
        { dispatch: false }
    )

    public readonly resetPassword$ = createEffect(() =>
        this.actions$.pipe(
            ofType(authActions.resetPassword),
            mergeMap(({ email }) =>
                from(sendPasswordResetEmail(this.auth, email)).pipe(
                    map(() => authActions.resetPasswordSuccess()),
                    catchError((error) => of(authActions.resetPasswordFailure({ error }))),
                )
            )
        )
    );

    public readonly uplaodResume$ = createEffect(() => this.actions$.pipe(
        ofType(authActions.uploadResume),
        switchMap(({ resume }) => this.userApiService.uploadResume(resume))
    ));

    public readonly uplaodResumeSuccess$ = createEffect(() => this.actions$.pipe(
        ofType(authActions.uploadResumeSuccess),
        tap(() => this.router.navigateByUrl(''))
    ),
        { dispatch: false }
    )

    public readonly signOut$ = createEffect(() =>
        this.actions$.pipe(
            ofType(authActions.signOut),
            mergeMap(() =>
                from(signOut(this.auth)).pipe(
                    tap(() => {
                        localStorage.removeItem(userLocalStorage);
                        localStorage.removeItem(emailVerifiedLocalStorage);
                        localStorage.removeItem(accessTokenLocalStorage);
                    }),
                    map(() => authActions.signOutSuccess()),
                    catchError((error) => of(authActions.signOutFailure({ error }))),
                )
            )
        )
    );

    public readonly signInSuccess$ = createEffect(() =>
        this.actions$.pipe(
            ofType(authActions.setCurrentUser),
            tap(() => this.notificationService.showSuccessMessage('Authentication successful'))
        ),
        { dispatch: false }
    );

    public readonly signInFailure$ = createEffect(() =>
        this.actions$.pipe(
            ofType(authActions.loadCurrentFailure),
            tap(({ error }) => {
                if (error?.message === 'email-not-verified') {
                    this.notificationService.showErrorMessage('Your email is not verified!');
                } else {
                    this.notificationService.showErrorMessage("You've entered wrong password! Please try again or reset your password.");
                }
            })
        ),
        { dispatch: false }
    );

    public readonly signUpSuccess$ = createEffect(() =>
        this.actions$.pipe(
            ofType(authActions.createUseruccess),
            tap(() => this.notificationService.showInfoMessage('Verification email has been sent'))
        ),
        { dispatch: false }
    );

    public readonly resetPasswordSuccess$ = createEffect(() =>
        this.actions$.pipe(
            ofType(authActions.resetPasswordSuccess),
            tap(() => this.notificationService.showSuccessMessage(`Link for resetting password was sent`))
        ),
        { dispatch: false }
    );
}
